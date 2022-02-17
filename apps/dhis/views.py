import json
import redis
from enum import IntEnum
from decouple import config

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0, decode_responses=True)


class Level(IntEnum):
    LOGIN = 1
    ORG_UNITS = 2
    DATA_SETS = 3
    PERIODS = 4
    SECTIONS = 5
    DATA_ELEMENTS = 6
    SAVE_OPTIONS = 7  # complete and incomplete


class Screen(object):
    def __init__(self, session_id, phone_number=None, user_response=None, level=None):
        self.session_id = session_id
        self.phone_number = phone_number
        self.user_response = user_response
        self.level = level
        self.state = {
            'passcode': '',
            'level': '',
            'org_unit': '',
            'data_element': '',
            'category_option_combo': '',
            'period': '',
            'dataset': '',
            'section': '',
        }

        if redis_instance.get(self.session_id):
            self.state = json.loads(redis_instance.get(self.session_id))

    def show(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError

    def proceed(self):
        raise NotImplementedError

    def ussd_proceed(self, display_text):
        self.save()
        display_text = "CON {}".format(display_text)
        response = Response(display_text, 200)
        response.headers['Content-Type'] = "text/plain"
        return response

    def ussd_end(self, display_text):
        redis_instance.delete(self.session_id)
        display_text = "END {}".format(display_text)
        response = Response(display_text, 200)
        response.headers['Content-Type'] = "text/plain"
        return response

    def save(self):
        if self.level == Level.LOGIN:
            self.state['level'] = self.level
            redis_instance.set(self.session_id, json.dumps(self.state))
        elif self.level == Level.ORG_UNITS:
            self.state['org_unit'] = self.user_response
            self.state['level'] = self.level
            redis_instance.set(self.session_id, json.dumps(self.state))


class LoginScreen(Screen):
    """serves the welcome screen"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.LOGIN)

    def show(self):
        menu_text = "Welcome to {}'s USSD service. Please enter your passcode:".format(
            config('INSTITUTE_NAME', 'Flare')
        )

        # print the response on to the page so that our gateway can read it
        return self.ussd_proceed(menu_text)

    def validate(self):
        if redis_instance.exists("usr_{}".format(self.user_response)):
            self.state['passcode'] = self.user_response
            self.save()
            return True
        return False

    def proceed(self):
        return OrgUnitScreen(session_id=self.session_id, phone_number=self.phone_number).show()


class OrgUnitScreen(Screen):
    """displays the org units that the user is assigned"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.ORG_UNITS)

    def show(self):
        key = "usr_{}".format(self.state['passcode'])
        if redis_instance.exists(key):
            org_units = json.loads(redis_instance.get(key))
            menu_text = "Select org unit:\n"
            for key, value in org_units.items():
                menu_text += "{}. {}\n".format(key, value['name'])

            return self.ussd_proceed(menu_text)

        return self.ussd_end("No org unit found.")

    def validate(self):
        key = "usr_{}".format(self.state['passcode'])
        if redis_instance.exists(key):
            org_units = json.loads(redis_instance.get(key))
            return self.user_response in org_units.keys()

        return False

    def proceed(self):
        pass


class Gateway(APIView):

    def post(self, req):
        session_id = req.data['sessionId']
        # service_code = req.data['serviceCode']
        phone_number = req.data['phoneNumber']

        list_of_inputs = req.data['text'].split("*")
        text = "*" if len(list_of_inputs) >= 2 and list_of_inputs[-1] == "" and list_of_inputs[-2] == "" else \
            list_of_inputs[-1]

        if text == "":
            screen = LoginScreen(session_id=session_id, phone_number=phone_number)
            return screen.show()

        screen = Screen(session_id=session_id, phone_number=phone_number)

        if screen.state['level'] == Level.LOGIN:
            screen = LoginScreen(session_id=session_id, phone_number=phone_number, user_response=text)
            if not screen.validate():
                return screen.show()
            else:
                return screen.proceed()

        if screen.state['level'] == Level.ORG_UNITS:
            screen = OrgUnitScreen(session_id=session_id, phone_number=phone_number, user_response=text)
            if not screen.validate():
                return screen.show()
            else:
                # return screen.proceed()
                return screen.ussd_end("Good bye 2")

        return screen.ussd_end("Good bye 1")
