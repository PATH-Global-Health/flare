from django.db import models
from settings.models import CommonModel

class Message(CommonModel):
    content = models.TextField(null=False)

    def __str__(self):
        return self.content