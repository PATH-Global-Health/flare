from django.apps import AppConfig


class MessageConfig(AppConfig):
    name = 'message'

    def ready(self):
        from . import signals
