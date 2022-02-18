from .screen.screen import Screen, Level
from .screen.login_screen import LoginScreen
from .screen.org_unit_screen import OrgUnitScreen


class USSDView:

    def __init__(self, session_id, phone_number, user_response=None):
        self.session_id = session_id
        self.phone_number = phone_number
        self.user_response = user_response

    def __show_initial(self):
        screen = LoginScreen(session_id=self.session_id, phone_number=self.phone_number)
        return screen.show()

    def __show_login(self):
        screen = LoginScreen(session_id=self.session_id, phone_number=self.phone_number,
                             user_response=self.user_response)
        if not screen.validate():
            return screen.show()
        else:
            return screen.next()

    def __show_org_units(self):
        screen = OrgUnitScreen(session_id=self.session_id, phone_number=self.phone_number,
                               user_response=self.user_response)
        if not screen.validate():
            return screen.show()
        else:
            # return screen.next()
            return screen.ussd_end("Good bye 2")

    def show(self):
        if self.user_response == "":
            return self.__show_initial()

        screen = Screen(session_id=self.session_id, phone_number=self.phone_number)

        if screen.state['level'] == Level.LOGIN:
            return self.__show_login()

        if screen.state['level'] == Level.ORG_UNITS:
            return self.__show_org_units()

        return screen.ussd_end("Good bye 1")
