from django.db import models
from apps.common.models import CommonModel


class OrgUnit(CommonModel):
    # survey_id = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=200, null=False)
    ou_id = models.CharField(max_length=40, null=False, unique=True)
    parent = models.CharField(max_length=40, null=False)

    def __str__(self):
        return self.name
