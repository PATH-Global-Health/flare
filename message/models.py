from django.db import models
from settings.models import CommonModel

class Message(CommonModel):
    content = models.TextField(null=False)
    status = models.CharField(max_length=255, null=True, blank=True)
    celery_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('created_at',)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.content