from rest_framework.views import APIView
from rest_framework.response import Response


class Gateway(APIView):

    def post(self, req):
        session_id = req.data['sessionId']
        service_code = req.data['serviceCode']
        phone_number = req.data['phoneNumber']

        text = req.data['text']

        response = ""

        if text == "":
            response = "CON What would you like to do?\n"
            response += "1. Check account details\n"
            response += "2. Check phone number\n"
            response += "3. Send me a message"

        elif text == "1":
            response = "CON What would you like to check on your account?\n"
            response += "1. Account number\n"
            response += "2. Account balance"

        elif text == "2":
            response = "END Your phone number is {}".format(phone_number)

        elif text == "3":
            try:
                sms_response = sms.send("Thank you for your response", sms_phone_number)
                print(sms_response)
            except Exception as e:
                print(f"Licio, we have a problem: {e}")

        elif text == "1*1":
            account_number = "1243324376742"
            response = "END Your account number is {}".format(account_number)

        elif text == "1*2":
            account_balance = "100,000"
            response = "END Your account balance is KES {}".format(account_balance)

        else:
            response = "END Invalid input. Try again."

        return Response(response)


