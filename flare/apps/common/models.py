from django.db import models
from django.contrib.auth.models import User


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.ForeignKey(User, related_name='created_%(class)s', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='updated_%(class)s', null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
