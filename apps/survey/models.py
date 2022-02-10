import os
from secrets import token_urlsafe

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.db.models.signals import pre_save

from apps.common.models import CommonModel
from apps.subscriber.models import Subscriber


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Survey(CommonModel):
    # survey_id = models.CharField(max_length=150, unique=True)
    title = models.CharField(max_length=200, null=False)
    slug = models.SlugField(blank=True, unique=True)
    published = models.BooleanField(default=False)
    # endpoint = models.CharField(max_length=150, default="")
    journeys = models.FileField(storage=OverwriteStorage())

    def __str__(self):
        return self.title


class SurveyResult(CommonModel):
    result = models.TextField(null=True)
    session_id = models.CharField(max_length=200, default="")
    phone_number = models.CharField(max_length=20, default="")
    completed = models.BooleanField(null=True)
    rejected = models.BooleanField(null=True)
    posted = models.BooleanField(null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(token_urlsafe(16))


pre_save.connect(pre_save_receiver, sender=Survey)
