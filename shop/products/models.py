from django.db import models
from shop.utils.models import StartedModel, AttributeExtraMixin


# Create your models here.


class Attribute(StartedModel, AttributeExtraMixin):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'

    def __str__(self):
        return self.key


class AttributeValue(StartedModel):
    label = models.TextField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    order = models.PositiveIntegerField(blank=True, null=True)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Attribute Value'
        verbose_name_plural = 'Attribute Values'

    def __str__(self):
        return self.label


class AttributeSet(StartedModel):
    name = models.CharField(max_length=255, unique=True)
    sub_attribute_set_type = models.ManyToManyField('self', blank=True, symmetrical=False)
    attribute = models.ManyToManyField('Attribute', blank=True, null=True)

    class Meta:
        verbose_name = 'Attribute Set'
        verbose_name_plural = 'Attribute Sets'

    def __str__(self):
        return self.name


class Product(StartedModel):
    name = models.CharField(max_length=255)
    base_code = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    sku = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    is_listable = models.BooleanField(default=False)
    attribute_sets = models.ForeignKey('AttributeSet',
                                       null=True,
                                       blank=True,
                                       on_delete=models.PROTECT)
    extra_attributes = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(StartedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(
        height_field="height",
        width_field="width",
        upload_to="products_image",
    )
    height = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class ProductVideo(StartedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='products_videos/')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Videos"
        verbose_name_plural = "Videos"

