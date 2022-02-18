from apps.subscriber.models import Subscriber
from apps.common import Language
import logging
import redis
from django.conf import settings
import time

redis_instance = redis


def change_language(ussd_request):
    try:
        lang = Language.objects.filter(pk=ussd_request.session['language']).first()
        if lang == None:
            return False
        phone_number = "+{}".format(ussd_request.session['phone_number'])

        redis_instance.set(phone_number, lang.code)

        sub = Subscriber.objects.filter(phone_number=phone_number).first()
        if sub == None:
            sub = Subscriber(phone_number=ussd_request.session['phone_number'])
        sub.language = lang

        sub.save()
    except Exception as ex:
        logging.exception(ex)
        return False

    return True
