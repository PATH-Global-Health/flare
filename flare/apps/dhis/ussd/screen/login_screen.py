import os


from django.conf import settings

from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store


class LoginScreen(Screen):
    """serves the welcome screen"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.LOGIN)

    def show(self):
        menu_text = "Welcome to {}'s USSD service. Please enter your passcode:".format(
            settings.INSTITUTE_NAME
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
        # used to restore an expired session
        key = "usr_state_{}".format(self.state['passcode'])
        if Store.exists(key) and Store.get(key) != self.session_id:
            from apps.dhis.ussd.screen import RestoreSessionScreen
            return RestoreSessionScreen(session_id=self.session_id, phone_number=self.phone_number).show()
        else:
            from apps.dhis.ussd.screen import OrgUnitScreen
            return OrgUnitScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        # We don't have any screens to return to because the login screen is the first one.
        return self.show()
