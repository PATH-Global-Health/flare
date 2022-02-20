from apps.dhis.ussd.screen.screen import Screen, Level
from apps.dhis.ussd.store.store import Store


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
                self.state['section'] = sections[self.user_response]['id']
                self.save()
                return True

        return False

    def next(self):
        return self.ussd_end("Go to the first data element")

    def prev(self):
        pass
