from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store


class OrgUnitScreen(Screen):
    """displays the org units that the user is assigned"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.ORG_UNITS)
        # store the current user state and session id
        Store.set("usr_state_{}".format(self.state['passcode']), self.session_id)
        org_unit_key = "usr_{}".format(self.state['passcode'])
        self.org_units = None

        if Store.exists(org_unit_key):
            self.org_units = Store.get(org_unit_key)

    def show(self):
        if self.org_units:
            menu_text = "Org unit:\n"
            for key, value in self.org_units.items():
                menu_text += "{}. {}\n".format(key, value['name'])

            return self.ussd_proceed(menu_text)

        return self.ussd_end("No org unit found.")

    def validate(self):
        if self.org_units:
            if self.user_response in self.org_units.keys():
                self.state['org_unit'] = self.org_units[self.user_response]['id']
                self.save()
                return True

        return False

    def next(self):
        from apps.dhis.ussd.screen import DatasetScreen
        return DatasetScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        # We should not return to the login screen from the org unit screen once we are authenticated successfully.
        return self.show()
