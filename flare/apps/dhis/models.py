import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.fields import ArrayField

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


class UserGroup(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    group_id = models.CharField(max_length=40, null=False, unique=True)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DHIS2User(CommonModel):
    objects = DHIS2Manager()

    name = models.CharField(max_length=200, null=True, blank=True)
    user_id = models.CharField(max_length=40, null=False, unique=True)
    username = models.CharField(max_length=100, null=False)
    passcode = models.CharField(max_length=30, null=True, unique=True)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)
    org_units = models.ManyToManyField(OrgUnit)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CategoryCombo(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    category_combo_id = models.CharField(
        max_length=40, null=False, unique=True)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CategoryOptionCombo(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    category_option_combo_id = models.CharField(max_length=40, null=False)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    category_combo = models.ForeignKey(CategoryCombo, on_delete=models.CASCADE)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class DataElement(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    data_element_id = models.CharField(max_length=40, null=False, unique=True)
    value_type = models.CharField(max_length=50, null=True, blank=True)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    category_combo = models.ForeignKey(
        CategoryCombo, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DataElementGroup(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    data_element_group_id = models.CharField(
        max_length=40, null=False, unique=True)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    data_element = models.ManyToManyField(DataElement)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# The user manually populates this model using the admin interface to ensure that the system only
# downloads data element groups that are part of this specific data element groupset.
class DataElementGroupSet(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    data_element_groupset_id = models.CharField(
        max_length=40, null=False, unique=True)
    data_element_groups = models.ManyToManyField(
        DataElementGroup, through='DataElementGroupGroupSet')
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Table to resolve the many-to-many relationship between data element group and data element groupset


class DataElementGroupGroupSet(CommonModel):
    objects = DHIS2Manager()
    sort_order = models.IntegerField(default=0)
    data_element_group = models.ForeignKey(
        DataElementGroup, on_delete=models.CASCADE)
    data_element_groupset = models.ForeignKey(
        DataElementGroupSet, on_delete=models.CASCADE)
    instance = models.ForeignKey(
        Instance, on_delete=models.CASCADE, null=True, blank=True)
    version = models.UUIDField(default=uuid.uuid4)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return "{} - {} - {}".format(self.data_element_group.name, self.data_element_groupset.name, self.sort_order)


class Dataset(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    dataset_id = models.CharField(max_length=40, null=False, unique=True)
    period_type = models.CharField(max_length=50, null=True, blank=True)
    open_future_periods = models.IntegerField(default=0)
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    org_units = models.ManyToManyField(OrgUnit)
    data_element = models.ManyToManyField(
        DataElement, through='DatasetDataElement')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Section(CommonModel):
    objects = DHIS2Manager()
    name = models.CharField(max_length=200, null=True, blank=True)
    section_id = models.CharField(max_length=40, null=False, unique=True)
    sort_order = models.IntegerField()
    version = models.UUIDField()
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.name


# To record the compulsory data elements (to validate data upon entry) as well as to render
# the list of data elements in the USSD views

# initialize_with_zero sets data elements to zero if value is true. Health facilities report zero
# for most data elements weekly. This ensures data elements are initialized with zero and users don't
# report all elements, making reporting faster.

class DatasetDataElement(CommonModel):
    objects = DHIS2Manager()
    sort_order = models.IntegerField(default=0)
    data_element = models.ForeignKey(DataElement, on_delete=models.CASCADE)
    data_set = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    category_option_combo = models.ForeignKey(
        CategoryOptionCombo, on_delete=models.CASCADE, null=True, blank=True)
    compulsory = models.BooleanField(default=False)
    initialize_with_zero = models.BooleanField(default=True)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, null=True, blank=True)
    instance = models.ForeignKey(
        Instance, on_delete=models.CASCADE, null=True, blank=True)
    version = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return "{} - {}".format(self.data_element.name, self.data_set.name)


class DataValueSet(CommonModel):
    objects = DHIS2Manager()
    data_set = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True)
    org_unit = models.ForeignKey(OrgUnit, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(DHIS2User, on_delete=models.CASCADE, null=True)
    period = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    mark_as_complete = models.BooleanField(default=False)
    status = models.CharField(
        max_length=8,
        choices=[("Pending", "Pending"), ("Synced", "Synced")],
        default="Pending",
    )

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return "{} - {} - {} - {}".format(self.data_set.name, self.org_unit.name, self.user.name, self.period)


class DataValue(CommonModel):
    objects = DHIS2Manager()
    data_element = models.ForeignKey(
        DataElement, on_delete=models.CASCADE, null=True)
    category_option_combo = models.ForeignKey(
        CategoryOptionCombo, on_delete=models.CASCADE, null=True)
    data_value_set = models.ForeignKey(
        DataValueSet, on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    session_id = models.CharField(max_length=240, null=True, blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return "{} - {} - {}".format(self.data_element.name, self.category_option_combo.name, self.value)
