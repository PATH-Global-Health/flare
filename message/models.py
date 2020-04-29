from django.db import models
from settings.models import CommonModel, Language

class Message(CommonModel):
    content = models.TextField(null=False)
    languages = models.ManyToManyField('settings.Language', related_name='messages', blank=True)

    def __str__(self):
        return self.content