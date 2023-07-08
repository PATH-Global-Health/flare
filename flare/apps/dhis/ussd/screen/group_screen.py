from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store


class GroupScreen(Screen):
    """displays the data element groups in the selected dataset"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.GROUPS)
        self.groups = None
        # The group_keys is a sequential number that is used to identify a data element group
        # and to present the user with options for selecting the data element groups the system
        # should display data elements from.
        self.group_keys = None

        dataset_de_group_key = "ds_deg_{}".format(self.state['dataset'])
        if Store.exists(dataset_de_group_key):
            self.groups = Store.get(dataset_de_group_key)
            self.group_keys = [str(val['sort_order'])
                               for val in self.groups.values()]

    def show(self):
        if self.groups:
            menu_text = "Groups:\n"
            for key, value in self.groups.items():
                menu_text += "{}. {}\n".format(
                    value['sort_order'], value['name'])
            menu_text += "#. Back"

            return self.ussd_proceed(menu_text)

        return self.ussd_end("No groups found.")

    def validate(self):
        if self.groups:
            if self.user_response in self.group_keys:
                # get the group key using the sort_order
                group_key = ''
                # The user selects the sequential number for the data element group. However, we wanted
                # to store the data element group ID we got from DHIS2.
                for key, val in self.groups.items():
                    if self.user_response == val['sort_order']:
                        group_key = key
                        break
                self.state['group'] = group_key
                # Always reset the data element index in the selected section to 0 to show the first data element.
                self.state['data_element_index'] = 0
                self.save()
                return True

        return False

    def next(self):
        # if the user selects 0, close the group screen
        if self.user_response == '0':
            from apps.dhis.ussd.screen import SaveOptionsScreen
            return SaveOptionsScreen(session_id=self.session_id, phone_number=self.phone_number).show()
        else:
            from apps.dhis.ussd.screen import GroupFormScreen
            return GroupFormScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        from apps.dhis.ussd.screen import FormTypeScreen
        return FormTypeScreen(session_id=self.session_id, phone_number=self.phone_number).show()
