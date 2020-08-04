__author__ = 'belendia@gmail.com'

from django.core.management.base import BaseCommand
from settings.models import Language, Channel, Configuration

CONFIGURATION = [
    {
        "language": 1,
        "channel": 2,
        "name": "Telegram - MOH Message - Amharic",
        "user_id": "",
        "token": ""
    },
    {
        "language": 2,
        "channel": 2,
        "name": "Telegram - MOH Message - Oromiffa",
        "user_id": "",
        "token": ""
    },
    {
        "language": 3,
        "channel": 2,
        "name": "Telegram - MOH Message - Tigrinya",
        "user_id": "",
        "token": ""
    }
]

class Command(BaseCommand):

    def handle(self, *args, **options):
        if Configuration.objects.count() == 0:
            for c in CONFIGURATION:
                lang = Language.objects.get(id=c['language'])
                chnl = Channel.objects.get(id=c['channel'])
                conf = Configuration(name=c['name'], user_id=c['user_id'], token=c['token'], language=lang, channel=chnl)
                conf.save()
                
                print('%s saved.' % (c['name']))
               
        else:
            print('Configuration table already initialized')