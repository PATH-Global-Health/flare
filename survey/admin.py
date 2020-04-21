from django.contrib import admin
from survey.models import Language, Subscriber, Survey, Message

admin.site.register(Language)
admin.site.register(Subscriber)
admin.site.register(Survey)
admin.site.register(Message)
