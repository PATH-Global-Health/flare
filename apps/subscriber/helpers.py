from apps.subscriber.models import Subscriber
from apps.settings import Language
import logging


def check_subscriber(phone):
    lang_code = "en"
    try:
        lang = Language.objects.filter(pk=1).first()
        sub = Subscriber.objects.filter(phone_number=phone).first()
        if sub is None:
            sub = Subscriber(phone_number=phone)
            sub.language = lang
            sub.save()
        lang_code = sub.language.code

    except Exception as ex:
        logging.exception(ex)

    return lang_code
