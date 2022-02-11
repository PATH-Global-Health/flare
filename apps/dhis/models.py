from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from apps.common.models import CommonModel


class DHIS2Manager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class DHIS2Instance(CommonModel):
    name = models.CharField(max_length=200, null=False)
    url = models.URLField(max_length=400)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class OrgUnit(CommonModel):
    objects = DHIS2Manager()

    name = models.CharField(max_length=200, null=False)
    ou_id = models.CharField(max_length=40, null=False, unique=True)
    parent = models.CharField(max_length=40, null=False)
    instance = models.ForeignKey(DHIS2Instance, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
