from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store


class SectionScreen(Screen):
    """displays the sections in the selected org unit"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.SECTIONS)

    def show(self):
        key = "ds_{}".format(self.state['dataset'])
        if Store.exists(key):
            sections = Store.get(key)
            menu_text = "Section:\n"
            for key, value in sections.items():
                menu_text += "{}. {}\n".format(key, value['name'])

            return self.ussd_proceed(menu_text)

        return self.ussd_end("No sections found.")

    def validate(self):
        key = "ds_{}".format(self.state['dataset'])
        if Store.exists(key):
            sections = Store.get(key)
            if self.user_response in sections.keys():
                # self.state['section'] = sections[self.user_response]['id']
                self.state['section'] = self.user_response
                # Always reset the data element index in the selected section to 0 to show the first data element.
                self.state['data_element_index'] = 0
                self.save()
                return True

        return False

    def next(self):
        # to fix circular import
        from apps.dhis.ussd.screen import DataElementScreen
        return DataElementScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        pass
