from django.db import models
from django.db.models import Prefetch


class OrderManager(models.Manager):
    def with_order_items(self, qs, *args, **kwargs):
        return qs.prefetch_related('order_items').all()
