from django.db import models
from shop.utils.models import StartedModel
# Create your models here.


class Merchant(StartedModel):
    name = models.CharField(max_length=255)
    extra_fields = models.JSONField(
        default=dict,
    )
    is_active = models.BooleanField(default=True)

