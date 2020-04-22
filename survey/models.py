from django.db import models
from settings.models import CommonModel
from subscriber.models import Subscriber

class Survey(CommonModel):
    title = models.CharField(max_length=20, null=False)
    yaml_file = models.CharField(max_length=20, default="{}")
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class SurveyResult(CommonModel):
    result = models.TextField()
    survey  = models.ForeignKey(Survey, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
