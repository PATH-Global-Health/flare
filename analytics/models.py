from django.db import models
from settings.models import CommonModel

class Report(CommonModel):
    total_messages = models.IntegerField()
    total_subscribers = models.IntegerField()
    total_surveys = models.IntegerField()
    total_suspects = models.IntegerField()
    suspects_by_region = models.TextField()
    suspects_by_sex = models.TextField()
    suspects_by_age = models.TextField()