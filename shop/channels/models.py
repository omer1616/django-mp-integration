from django.db import models
from shop.utils.models import StartedModel
# Create your models here.
from .enums import ChannelType
from enumfields import EnumField
from django.utils.module_loading import import_string


class Channel(StartedModel):
    merchant = models.ForeignKey('merchants.Merchant', on_delete=models.CASCADE)
    channel_type = EnumField(ChannelType)
    name = models.CharField(max_length=255)
    conf = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'

    def __str__(self):
        return self.name

