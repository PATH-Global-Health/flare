from apps.dhis.ussd.screen.screen import Screen, Level
from apps.dhis.ussd.store.store import Store
from apps.dhis.utils import validate_data_element_by_value_type


class DataElementScreen(Screen):
    """displays the data elements in the selected section"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.DATA_ELEMENTS)

    def show(self):
        key = "ds_{}".format(self.state['dataset'])
        if Store.exists(key):
            sections = Store.get(key)

            if self.state['section'] in sections.keys():
                data_elements = sections[self.state['section']]['data_elements']
                data_element_index = int(self.state['data_element_index'])

                # If the previous data element has an error don't progress to the next data element.
                if self.state['previous_data_element_value_error'] is False:
                    data_element_index += 1

                if data_element_index >= len(data_elements):
                    # show section or save options (complete vs incomplete) screen
                    pass
                print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                print(data_elements[data_element_index])
                # append the category option combination name is not default, then append it to the data element name
                menu_text = data_elements[data_element_index]['data_element_name']
                cat_opt_combo_name = data_elements[data_element_index]['category_option_combo_name']
                menu_text += " - {}".format(cat_opt_combo_name) if cat_opt_combo_name != 'default' else ""
                print(menu_text)
                # save state
                self.state['data_element_index'] = data_element_index
                self.state['previous_data_element_value_error'] = False  # reset this variable

                return self.ussd_proceed(menu_text)

        return self.ussd_end("No sections found.")

    def validate(self):
        key = "ds_{}".format(self.state['dataset'])
        if Store.exists(key):
            sections = Store.get(key)
            if self.state['section'] in sections.keys():
                data_elements = sections[self.state['section']]['data_elements']
                data_element_index = int(self.state['data_element_index'])
                data_element_value_type = data_elements[data_element_index]['data_element_value_type']

                # validate the data element
                result = validate_data_element_by_value_type(data_element_value_type, self.user_response)

                if result[0]:
                    data_element = data_elements[data_element_index]['data_element_id']
                    category_option_combo = data_elements[data_element_index]['category_option_combo_id']
                    org_unit = self.state['org_unit']
                    period = self.state['period']

                    key = "{}-{}".format(data_element, category_option_combo)
                    # If true the show method will display the data element that it showed previously. It doesn't
                    # progress forward and show the next data element.
                    self.state['previous_data_element_value_error'] = False
                    self.state['data_element_values'][key] = result[1]
                    self.save()

                    # save into database
                    # save_to_database.delay(data_element, category_option_combo, org_unit, period, result[1])
                    return False

                # the previous screen has value error. Show the current data element and try to get a new value again.
                self.state['previous_data_element_value_error'] = True
                self.save()
                return False

        return False

    def next(self):
        return self.ussd_end("Go to the first data element")

    def prev(self):
        pass
