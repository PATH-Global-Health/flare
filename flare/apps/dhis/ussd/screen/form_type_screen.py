from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store
from apps.dhis.utils import get_data_from_dhis2
from apps.dhis.models import DataValueSet
from apps.dhis.tasks import save_values_to_database_batch


class FormTypeScreen(Screen):
    """displays the form types like Group Form, Section Form or Default Form"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.FORM_TYPES)
        self.sections = None
        section_key = "ds_{}".format(self.state['dataset'])
        if Store.exists(section_key):
            self.sections = Store.get(section_key)

        self.__initialize_data_values()

    def __initialize_data_values(self):
        # Resetting data values is useful for preventing values from one dimension leaking into another when a user
        # switches between orgunits, datasets, or periods.
        self.reset_data_values()

        # If any data values are stored in the Flare app database, retrieve and store them in Redis.
        data_value_sets = DataValueSet.objects.filter(
            data_set__dataset_id=self.state['dataset'], org_unit__org_unit_id=self.state['org_unit'], period=self.state['period'])
        if data_value_sets.count() > 0:
            dvs = data_value_sets[0]
            for dv in dvs.datavalue_set.all():
                key = '{}-{}'.format(dv.data_element.data_element_id,
                                     dv.category_option_combo.category_option_combo_id)
                self.state['data_values'][key] = dv.value

        # Retrieve information from DHIS2 and save it in Redis, allowing the user to make updates as needed.
        # Cache data retrieved from DHIS2, if the same data is not found in the Flare database.
        dhis2_data = get_data_from_dhis2(
            self.state['passcode'], self.state['dataset'], self.state['org_unit'], self.state['period'])
        if 'dataValues' in dhis2_data:
            for data_value in dhis2_data['dataValues']:
                key = '{}-{}'.format(data_value['dataElement'],
                                     data_value['categoryOptionCombo'])
                if key not in self.state['data_values']:
                    self.state['data_values'][key] = data_value['value']

        self.save()

    def __store_data_elements(self, data_elements):
        # Save into database
        if len(data_elements) > 0:
            save_values_to_database_batch.delay(
                self.state['dataset'], self.state['org_unit'], self.state['passcode'], self.state['period'], self.phone_number, data_elements)
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
            group_screen = GroupScreen(
                session_id=self.session_id, phone_number=self.phone_number)
            data_elements = group_screen.initialize_with_zero()
            self.__store_data_elements(data_elements)
            return group_screen.show()
        else:
            # Show the section screen only if the dataset has section
            if self.state['has_section']:
                from apps.dhis.ussd.screen import SectionScreen
                # clear sections visited list
                self.state['sections_visited'].clear()
                session_screen = SectionScreen(
                    session_id=self.session_id, phone_number=self.phone_number)
                data_elements = session_screen.initialize_with_zero()
                self.__store_data_elements(data_elements)
                return session_screen.show()
            else:
                from apps.dhis.ussd.screen import DefaultFormScreen
                default_form_screen = DefaultFormScreen(
                    session_id=self.session_id, phone_number=self.phone_number)
                data_elements = default_form_screen.initialize_with_zero()
                self.__store_data_elements(data_elements)
                return default_form_screen.show()

    def prev(self):
        from apps.dhis.ussd.screen import PeriodScreen
        return PeriodScreen(session_id=self.session_id, phone_number=self.phone_number).show()
