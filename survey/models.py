import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from settings.models import CommonModel
from subscriber.models import Subscriber

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
   
class Survey(CommonModel):
    title = models.CharField(max_length=20, null=False)
    journeys = models.FileField(upload_to='journeys', storage=OverwriteStorage())

    def __str__(self):
        return self.title

class SurveyResult(CommonModel):
    result = models.TextField()
    survey  = models.ForeignKey(Survey, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
