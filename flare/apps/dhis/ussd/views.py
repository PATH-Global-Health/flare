from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.utils import get_screen


class USSDView:

    def __init__(self, session_id, phone_number, user_response=None):
        self.session_id = session_id
        self.phone_number = phone_number
        self.user_response = user_response
        self.screen = Screen(session_id=self.session_id, phone_number=self.phone_number)

    def show(self):

        self.screen = get_screen(self.session_id, self.phone_number, self.user_response, self.screen.state['level'])

        # If the user enters #, go back one screen.
        if self.user_response == "#":
            return self.screen.prev()

        if not self.screen.validate():
            return self.screen.show()
        else:
            return self.screen.next()
