from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store


class SectionScreen(Screen):
    """displays the sections in the selected org unit"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.SECTIONS)
        self.sections = None
        section_key = "ds_{}".format(self.state['dataset'])
        if Store.exists(section_key):
            self.sections = Store.get(section_key)

    def show(self):
        if self.sections:
            menu_text = "Section:\n"
            for key, value in self.sections.items():
                menu_text += "{}. {}\n".format(key, value['name'])
            menu_text += "#. Back"

            return self.ussd_proceed(menu_text)

        return self.ussd_end("No sections found.")

    def validate(self):
        if self.sections:
            if self.user_response in self.sections.keys():
                # self.state['section'] = sections[self.user_response]['id']
                self.state['section'] = self.user_response
                # Always reset the data element index in the selected section to 0 to show the first data element.
                self.state['data_element_index'] = 0
                self.save()
                return True

        return False

    def next(self):
        # to fix circular import
        from apps.dhis.ussd.screen import SectionFormScreen
        return SectionFormScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        from apps.dhis.ussd.screen import FormTypeScreen
        return FormTypeScreen(session_id=self.session_id, phone_number=self.phone_number).show()
