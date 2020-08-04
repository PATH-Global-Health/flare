__author__ = 'belendia@gmail.com'

from django.core.management.base import BaseCommand
from settings.models import Channel

CHANNEL = [
    {
        "name": "Africa's Talking / SMS",
    },
    {
        "name": "Telegram",
    }
]

class Command(BaseCommand):

    def handle(self, *args, **options):
        if Channel.objects.count() == 0:
            for chnl in CHANNEL:
                channel = Channel(name=chnl['name'])
                channel.save()
                
                print('%s saved.' % (chnl['name']))
               
        else:
            print('Channel table already initialized')