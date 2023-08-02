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

    # Because most of the data elements reported are zero, we should initialize them to zero.
    # Users should only report data elements that have a case.
    def initialize_with_zero(self):
        data_elements = []

        for section_key, section in self.sections.items():
            for de in section['data_elements']:
                key = '{}-{}'.format(de['data_element_id'],
                                     de['category_option_combo_id'])
                if de['initialize_with_zero'] and key not in self.state['data_values']:
                    self.state['data_values'][key] = 0
                    data_elements.append({
                        'data_element': de['data_element_id'],
                        'category_option_combo': de['category_option_combo_id'],
                        'value': 0,
                        'session_id': self.session_id
                    })

        return data_elements

    def generate_menu_item(self):
        for key, value in self.sections.items():
            self.menu_items.append("{}. {}".format(key, value['name']))

    def show(self):
        if self.sections:
            self.generate_menu_item()
            paginated_menu = self.paginate_menu_item(self.user_response)
            # Add a menu title at the beginning of the menu options
            paginated_menu.insert(0, "Section:")
            # Add back option at the end
            paginated_menu.append("#. Back")

            return self.ussd_proceed("\n".join(paginated_menu))

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
