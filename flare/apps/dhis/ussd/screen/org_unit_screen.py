from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store


class OrgUnitScreen(Screen):
    """displays the org units that the user is assigned"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.ORG_UNITS)
        # store the current user state and session id
        Store.set("usr_state_{}".format(
            self.state['passcode']), self.session_id)
        org_unit_key = "usr_{}".format(self.state['passcode'])
        self.org_units = None

        if Store.exists(org_unit_key):
            self.org_units = Store.get(org_unit_key)

    def generate_menu_item(self):
        for key, value in self.org_units.items():
            self.menu_items.append("{}. {}".format(key, value['name']))

    def show(self):
        if self.org_units:
            self.generate_menu_item()
            paginated_menu = self.paginate_menu_item(self.user_response)
            # Add a menu title at the beginning of the menu options
            paginated_menu.insert(0, "Org unit:")

            return self.ussd_proceed("\n".join(paginated_menu))

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
