from django.db import models
from settings.models import CommonModel, Language

class Subscriber(CommonModel):
    phone_number = models.IntegerField(unique=True, null=False)
    language  = models.ForeignKey( Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number
