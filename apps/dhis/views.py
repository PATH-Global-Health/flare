from rest_framework.views import APIView

from apps.dhis.ussd import USSDView


class Gateway(APIView):

    def post(self, req):
        session_id = req.data['sessionId']
        # service_code = req.data['serviceCode']
        phone_number = req.data['phoneNumber']

        list_of_inputs = req.data['text'].split("*")
        text = "*" if len(list_of_inputs) >= 2 and list_of_inputs[-1] == "" and list_of_inputs[-2] == "" else \
            list_of_inputs[-1]

        ussd_view = USSDView(session_id, phone_number, text)
        return ussd_view.show()
