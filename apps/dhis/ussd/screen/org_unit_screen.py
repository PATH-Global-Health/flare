from .screen import Screen, Level
from .dataset_screen import DatasetScreen
from ..store.store import Store


class OrgUnitScreen(Screen):
    """displays the org units that the user is assigned"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.ORG_UNITS)

    def show(self):
        key = "usr_{}".format(self.state['passcode'])
        if Store.exists(key):
            org_units = Store.get(key)
            menu_text = "Select org unit:\n"
            for key, value in org_units.items():
                menu_text += "{}. {}\n".format(key, value['name'])

            return self.ussd_proceed(menu_text)

        return self.ussd_end("No org unit found.")

    def validate(self):
        key = "usr_{}".format(self.state['passcode'])
        if Store.exists(key):
            org_units = Store.get(key)
            if self.user_response in org_units.keys():
                self.state['org_unit'] = org_units[self.user_response]['id']
                self.save()
                return True

        return False

    def next(self):
        return DatasetScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        pass
