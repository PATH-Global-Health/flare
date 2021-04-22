from django.db import models
from django.contrib.auth.models import User


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.ForeignKey(User, related_name='created_%(class)s', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='updated_%(class)s', null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Language(CommonModel):
    name = models.CharField(max_length=50, unique=True, null=False)
    code = models.CharField(max_length=10, unique=True, null=False)
    messages = models.ManyToManyField('message.Message', related_name='languages', blank=True)

    def __str__(self):
        return self.name


class Channel(CommonModel):
    name = models.CharField(max_length=128)
    channel_setting = models.ManyToManyField(Language, through='Configuration', blank=True)
    messages = models.ManyToManyField('message.Message', related_name='channels', blank=True)

    def __str__(self):
        return self.name


class Configuration(CommonModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    user_id = models.CharField(max_length=100, null=False)
    token = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.name
