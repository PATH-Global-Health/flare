import os
from django.http import HttpResponse
from ussd.core import UssdView, UssdRequest
from django.conf import settings
import redis
from subscriber.helpers import check_subscriber

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0, decode_responses=True)

class GatewayCovid19View(UssdView):
    customer_journey_conf = os.path.join(settings.BASE_DIR, 'journeys/covid19.yml')
    customer_journey_namespace = 'demo-customer-journey'

    def post(self, req):
        list_of_inputs = req.data['text'].split("*")
        text = "*" if len(list_of_inputs) >= 2 and \
                      list_of_inputs[-1] == "" and \
                      list_of_inputs[-2] == "" else list_of_inputs[
            -1]
   
        if len(req.data['text'])==0:
            lang_code = check_subscriber(req.data['phoneNumber'])
            redis_instance.set(req.data['phoneNumber'], lang_code)

        session_id = req.data['sessionId']
        language = redis_instance.get(req.data['phoneNumber'])
       
        if req.data.get('use_built_in_session_management', False):
            session_id = None
        ussd_request = UssdRequest(
            phone_number=req.data['phoneNumber'].strip('+'),
            session_id=session_id,
            ussd_input=text,
            raw_input=req.data['text'],
            service_code=req.data['serviceCode'],
            language=language,
            use_built_in_session_management=req.data.get(
                'use_built_in_session_management', False),
        )

        return ussd_request

    def ussd_response_handler(self, ussd_response):

        if self.request.data.get('serviceCode') == 'test':
            return super(GatewayCovid19View, self).\
                ussd_response_handler(ussd_response)
        if ussd_response.status:
            res = 'CON' + ' ' + str(ussd_response)
            response = HttpResponse(res)
        else:
            redis_instance.delete(self.request.data.get('phoneNumber'))
            res = 'END' + ' ' + str(ussd_response)
            response = HttpResponse(res)
        return response

