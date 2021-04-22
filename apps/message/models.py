from django.db import models
from apps.settings import CommonModel, Configuration

class Message(CommonModel):
    content = models.TextField(null=False)
    status = models.CharField(max_length=255, null=True, blank=True)
    celery_id = models.CharField(max_length=255, null=True, blank=True)
    status_detail = models.ManyToManyField(Configuration, through = 'MessageStatus', blank=True)

    class Meta:
        ordering = ['created_at']

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.content

class MessageStatus(CommonModel):
    message = models.ForeignKey(Message, on_delete = models.CASCADE)
    configuration = models.ForeignKey(Configuration, on_delete = models.CASCADE, null=True)
    success_count = models.IntegerField()
    error_count = models.IntegerField()
    config_error = models.BooleanField(null=True)
    