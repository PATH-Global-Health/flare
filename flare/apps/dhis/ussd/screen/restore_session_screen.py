from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store
from apps.dhis.utils import get_screen


class RestoreSessionScreen(Screen):
    """used to restore the previous session"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.RESTORE)

    def show(self):
        menu_text = "Would you like to resume where you left off?\n1. Yes\n2. No"

        # print the response on to the page so that our gateway can read it
        return self.ussd_proceed(menu_text)

    def validate(self):
        if self.user_response in ['1', '2']:
            return True
        return False

    def next(self):
        key = "usr_state_{}".format(self.state['passcode'])
        if self.user_response == '1':
            # restore the previous session

            previous_session_id = Store.get(key)
            self.state = Store.get(previous_session_id)
            self.save(self.state['level'])

            # store the current user state and session id
            Store.set(key, self.session_id)

            # delete the previous session state and user state which stores the previous session id
            Store.delete(previous_session_id)

            return get_screen(self.session_id, self.phone_number, self.user_response, self.state['level']).show()
        else:
            Store.delete(key)

            from apps.dhis.ussd.screen import OrgUnitScreen
            return OrgUnitScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        return self.show()
