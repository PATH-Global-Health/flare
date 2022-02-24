from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store


class SaveOptionsScreen(Screen):
    """displays the save options to the user"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.SAVE_OPTIONS)

    def show(self):
        menu_text = "Save options:\n"
        menu_text += "1. Complete\n"
        menu_text += "2. Save"

        return self.ussd_proceed(menu_text)

    def validate(self):
        if self.user_response in ['1', '2']:
            return True

        return False

    def next(self):
        return self.ussd_end("Thank you")

    def prev(self):
        pass
