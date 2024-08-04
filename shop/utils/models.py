from django.db import models

class StartedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta(object):
        abstract = True


class AttributeExtraMixin(models.Model):
    is_required = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    is_searchable = models.BooleanField(default=True)
    is_filterable = models.BooleanField(default=False)
    is_variant = models.BooleanField(default=False)
    is_listable = models.BooleanField(default=False)
    is_form_required = models.BooleanField(default=False)

    class Meta:
        abstract = True
