__author__ = 'belendia@gmail.com'

from django.core.management.base import BaseCommand
from settings.models import Language

LANGUAGES = [
    {
        "pk": 1,
        "name": "Amharic",
        "code": "am",
    },
    {
        "pk": 2,
        "name": "Oromifa",
        "code": "or",
    },
    {
        "pk": 3,
        "name": "Tigrigna",
        "code": "ti",
    },
    {
        "pk": 4,
        "name": "Somali",
        "code": "so",
    },
    {
        "pk": 5,
        "name": "Afar",
        "code": "aa",
    },
    {
        "pk": 6,
        "name": "English",
        "code": "en",
    }
]

class Command(BaseCommand):

    def handle(self, *args, **options):
        if Language.objects.count() == 0:
            for lang in LANGUAGES:
                language = Language(name=lang['name'], code=lang['code'])
                language.save()
                
                print('Language name %s saved.' % (lang['name']))
               
        else:
            print('Language table already initialized')