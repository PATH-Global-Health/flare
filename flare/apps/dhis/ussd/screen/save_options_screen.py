from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store
from apps.dhis.tasks import save_mark_as_complete_to_database


class SaveOptionsScreen(Screen):
    """displays the save options to the user"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.SAVE_OPTIONS)

    def show(self):
        menu_text = "Save options:\n"
        menu_text += "1. Complete\n"
        menu_text += "2. Save\n"
        menu_text += "#. Back"

        return self.ussd_proceed(menu_text)

    def validate(self):
        if self.user_response in ['1', '2']:
            save_mark_as_complete_to_database.delay(self.state['dataset'], self.state['org_unit'],
                                                    self.state['passcode'], self.state['period'], self.user_response)
            return True

        return False

    def next(self):
        return self.ussd_end("Thank you")

    def prev(self):
        # Show section form if the dataset has one; otherwise, show default form
        if self.state['has_section']:
            from apps.dhis.ussd.screen import SectionFormScreen
            # clear sections visited list
            self.state['sections_visited'].clear()
            return SectionFormScreen(session_id=self.session_id, phone_number=self.phone_number).show()
        else:
            from apps.dhis.ussd.screen import DefaultFormScreen
            return DefaultFormScreen(session_id=self.session_id, phone_number=self.phone_number).show()
