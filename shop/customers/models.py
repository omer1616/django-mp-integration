from django.db import models
from enumfields import EnumField
from shop import channels
from shop.utils.models import StartedModel
# Create your models here.
from .enums import GenderType


class Customer(StartedModel):
    channel = models.ForeignKey('channels.Channel', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    remote_id = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    gender = EnumField(GenderType, blank=True, null=True)

    class Meta:
        unique_together = (('remote_id', 'channel'),)

