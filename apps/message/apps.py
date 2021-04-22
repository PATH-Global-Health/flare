from django.apps import AppConfig


class MessageConfig(AppConfig):
    name = 'apps.message'

    def ready(self):
        from . import signals
