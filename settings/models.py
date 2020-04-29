from django.db import models
from django.contrib.auth.models import User

class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, related_name='created_%(class)s',null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='updated_%(class)s',null=True, on_delete=models.SET_NULL)
    class Meta:
        abstract = True

class Language(CommonModel):
   
    name = models.CharField(max_length=50, unique=True, null=False)
    code = models.CharField(max_length =10, unique=True, null=False)
    messages = models.ManyToManyField('message.Message', related_name='languages', blank=True)

    def __str__(self):
        return self.name
