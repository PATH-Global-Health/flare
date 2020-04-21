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

    def __str__(self):
        return self.name


class Subscriber(CommonModel):
    telephone = models.CharField(max_length=20, unique=True, null=False)
    language  = models.ForeignKey( Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.telephone

class Survey(CommonModel):
    title = models.CharField(max_length=20, null=False)
    questions = models.TextField(null = False)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Message(CommonModel):
    content = models.TextField(null=False)

    def __str__(self):
        return self.content
