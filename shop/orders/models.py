from django.db import models
from django.db.models import Min, Max
from enumfields import EnumField
from .enums import OrderStatus
from shop.customers.models import Customer
from shop.utils.models import StartedModel
from .managers import OrderManager


# Create your models here.

class Order(StartedModel):
    order_number = models.CharField(max_length=255)
    channel = models.ForeignKey('channels.Channel', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True)
    status = EnumField(OrderStatus)
    extra_field = models.JSONField(default=dict)
    objects = OrderManager()

    class Meta:
        unique_together = (('order_number', 'channel'),)


class OrderItem(StartedModel):
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, related_name='order_items')
    status = EnumField(OrderStatus)
    sku = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    remote_order_item_id = models.CharField(max_length=255, blank=True, null=True)
    extra_field = models.JSONField(default=dict)
