from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store
from apps.dhis.utils import validate_data_element_by_value_type
from apps.dhis.tasks import save_values_to_database


class DefaultFormScreen(Screen):
    """displays the data elements in a dataset which do not have any section"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.DEFAULT_FORM)
        dataset_key = "ds_{}".format(self.state['dataset'])
        self.dataset = None

        if Store.exists(dataset_key):
            self.dataset = Store.get(dataset_key)
            self.data_elements = self.dataset['data_elements']
            self.data_element_index = int(self.state['data_element_index'])
            self.data_element_value_type = self.data_elements[self.data_element_index]['data_element_value_type']
            self.compulsory = self.data_elements[self.data_element_index]['compulsory']
            self.data_element = self.data_elements[self.data_element_index]['data_element_id']
            self.category_option_combo = self.data_elements[self.data_element_index]['category_option_combo_id']


    def show(self):
        if self.dataset:
            if self.data_element_index < len(self.data_elements):
                # If the category option combination name is not default, then append it to the data element
                # name
                data_element_name = self.data_elements[self.data_element_index]['data_element_name']
                menu_text = " * {}".format(data_element_name) if self.compulsory else data_element_name

                cat_opt_combo_name = self.data_elements[self.data_element_index]['category_option_combo_name']
                menu_text += " - {}".format(cat_opt_combo_name) if cat_opt_combo_name != 'default' else ""

                return self.ussd_proceed(menu_text)
            else:
                self.next()

        return self.ussd_end("Dataset not found")

    # validate will always return false until all data elements are filled
    def validate(self):
        if self.dataset:
            # validate the data element
            result = validate_data_element_by_value_type(self.compulsory, self.data_element_value_type, self.user_response)

            if result[0]:
                # save the value that is received from the user in the state. The key is a concatenation of
                # data element and category option combo ids.
                key = "{}-{}".format(self.data_element, self.category_option_combo)
                self.state['data_element_values'][key] = result[1]
                self.save()

                # save into database
                save_values_to_database.delay(self.state['dataset'], self.data_element, self.category_option_combo,
                                              self.state['org_unit'], self.state['passcode'], self.state['period'],
                                              result[1], self.phone_number, self.session_id)
                return True

        return False

    def next(self):
        if self.dataset:
            self.data_element_index += 1

            # If all data elements in the selected sections are visited, increment the index and loop
            if self.data_element_index < len(self.data_elements):
                # save state
                self.state['data_element_index'] = self.data_element_index
                self.save()

                return self.show()
            else:
                from apps.dhis.ussd.screen import SaveOptionsScreen
                return SaveOptionsScreen(session_id=self.session_id, phone_number=self.phone_number).show()
        return self.ussd_end("No data sets are found")

    def prev(self):
        pass
