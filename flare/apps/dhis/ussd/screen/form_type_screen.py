from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store
from apps.dhis.utils import get_data_from_dhis2


class FormTypeScreen(Screen):
    """displays the form types like Group Form, Section Form or Default Form"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.FORM_TYPES)
        self.sections = None
        section_key = "ds_{}".format(self.state['dataset'])
        if Store.exists(section_key):
            self.sections = Store.get(section_key)

        # Retrieve information from DHIS2 and save it in Redis, allowing the user to make updates as needed.
        dhis2_data = get_data_from_dhis2(
            self.state['passcode'], self.state['dataset'], self.state['org_unit'], self.state['period'])
        if 'dataValues' in dhis2_data:
            for data_value in dhis2_data['dataValues']:
                key = '{}-{}'.format(data_value['dataElement'],
                                     data_value['categoryOptionCombo'])
                if key not in self.state['data_element_values']:
                    self.state['data_element_values'][key] = data_value['value']
            self.save()

    def show(self):
        default_or_section_form_type = 'Section' if self.state['has_section'] else 'Default'
        menu_text = "Form Type:\n"
        menu_text += "1. Group\n"
        menu_text += "2. {}\n".format(default_or_section_form_type)
        menu_text += "#. Back"

        return self.ussd_proceed(menu_text)

    def validate(self):
        if self.sections:
            if self.user_response in ['1', '2']:
                return True

        return False

    def next(self):
        if self.user_response == '1':
            # to fix circular import
            from apps.dhis.ussd.screen import GroupScreen
            # clear groups visited list
            self.state['groups_visited'].clear()
            return GroupScreen(session_id=self.session_id, phone_number=self.phone_number).show()
        else:
            # Show the section screen only if the dataset has section
            if self.state['has_section']:
                from apps.dhis.ussd.screen import SectionScreen
                # clear sections visited list
                self.state['sections_visited'].clear()
                return SectionScreen(session_id=self.session_id, phone_number=self.phone_number).show()
            else:
                from apps.dhis.ussd.screen import DefaultFormScreen
                return DefaultFormScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        from apps.dhis.ussd.screen import PeriodScreen
        return PeriodScreen(session_id=self.session_id, phone_number=self.phone_number).show()
