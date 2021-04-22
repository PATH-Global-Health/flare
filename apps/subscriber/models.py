from django.db import models
from apps.settings import CommonModel, Language

class Subscriber(CommonModel):
    phone_number = models.CharField(max_length = 20, unique=True, null=False)
    language  = models.ForeignKey( Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number
