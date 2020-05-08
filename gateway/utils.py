from subscriber.models import Subscriber
from settings.models import Language
import logging

def change_language(ussd_request):
    try:
        lang  = Language.objects.filter(pk=ussd_request.session['language']).first()
        if lang == None:
            return False
        sub  = Subscriber.objects.filter(phone_number="+{}".format(ussd_request.session['phone_number'])).first()
        if sub == None:
            sub = Subscriber(phone_number=ussd_request.session['phone_number'])
        sub.language=lang
        sub.save()
    except Exception as ex:
        logging.exception(ex)
        return False
   
    return True