import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from apps.common.models import CommonModel


class DHIS2Manager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class Instance(CommonModel):
    name = models.CharField(max_length=200, null=False)
    url = models.URLField(max_length=400)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class OrgUnit(CommonModel):
    objects = DHIS2Manager()

    name = models.CharField(max_length=200, null=False)
    org_unit_id = models.CharField(max_length=40, null=False, unique=True)
    parent = models.CharField(max_length=40, null=False)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DHIS2User(CommonModel):
    objects = DHIS2Manager()

    name = models.CharField(max_length=200, null=True, blank=True)
    user_id = models.CharField(max_length=40, null=False, unique=True)
    username = models.CharField(max_length=100, null=False)
    passcode = models.CharField(max_length=30, null=False)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    org_units = models.ManyToManyField(OrgUnit)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Dataset(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    dataset_id = models.CharField(max_length=40, null=False, unique=True)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    org_units = models.ManyToManyField(OrgUnit)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CategoryCombo(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    category_combo_id = models.CharField(max_length=40, null=False, unique=True)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)


class DataElement(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    data_element_id = models.CharField(max_length=40, null=False, unique=True)
    value_type = models.CharField(max_length=50, null=True, blank=True)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    dataset = models.ManyToManyField(Dataset)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
