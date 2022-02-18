from decouple import config

from .screen import Screen, Level
from .org_unit_screen import OrgUnitScreen
from ..store.store import Store


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
        if Store.exists("usr_{}".format(self.user_response)):
            self.state['passcode'] = self.user_response
            self.save()
            return True
        return False

    def next(self):
        return OrgUnitScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        pass
