from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store
from apps.dhis.utils import validate_data_element_by_value_type
from apps.dhis.tasks import save_values_to_database


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

                if data_element_index < len(data_elements):
                    # append the category option combination name is not default, then append it to the data element
                    # name
                    menu_text = data_elements[data_element_index]['data_element_name']
                    cat_opt_combo_name = data_elements[data_element_index]['category_option_combo_name']
                    menu_text += " - {}".format(cat_opt_combo_name) if cat_opt_combo_name != 'default' else ""

                    return self.ussd_proceed(menu_text)
                else:
                    self.next()

        return self.ussd_end("No data sets found")

    # validate will always return false until all data elements are filled
    def validate(self):
        key = "ds_{}".format(self.state['dataset'])
        if Store.exists(key):
            sections = Store.get(key)
            if self.state['section'] in sections.keys():

                # if the current section selected is not in the section visited list, add it
                if self.state['section'] not in self.state['sections_visited']:
                    self.state['sections_visited'].append(self.state['section'])

                data_elements = sections[self.state['section']]['data_elements']
                data_element_index = int(self.state['data_element_index'])
                data_element_value_type = data_elements[data_element_index]['data_element_value_type']

                # validate the data element
                result = validate_data_element_by_value_type(data_element_value_type, self.user_response)

                if result[0]:
                    data_element = data_elements[data_element_index]['data_element_id']
                    category_option_combo = data_elements[data_element_index]['category_option_combo_id']

                    # save the value that is received from the user in the state. The key is a concatenation of
                    # data element and category option combo ids.
                    key = "{}-{}".format(data_element, category_option_combo)
                    self.state['data_element_values'][key] = result[1]
                    self.save()

                    # save into database
                    save_values_to_database.delay(self.state['dataset'], data_element, category_option_combo,
                                                  self.state['org_unit'], self.state['passcode'], self.state['period'],
                                                  result[1], self.phone_number, self.session_id)
                    return True

        return False

    def next(self):

        key = "ds_{}".format(self.state['dataset'])
        if Store.exists(key):
            sections = Store.get(key)

            if self.state['section'] in sections.keys():
                data_elements = sections[self.state['section']]['data_elements']
                data_element_index = int(self.state['data_element_index'])

                data_element_index += 1

                # If all data elements in the selected sections are visited, increment the index and loop
                if data_element_index < len(data_elements):
                    # save state
                    self.state['data_element_index'] = data_element_index
                    self.save()

                    return self.show()
                else:
                    # reset the data element index
                    self.state['data_element_index'] = 0

                    # If all sections are visited, show the save options screen
                    if len(sections.keys()) == len(self.state['sections_visited']):
                        from apps.dhis.ussd.screen import SaveOptionsScreen
                        return SaveOptionsScreen(session_id=self.session_id, phone_number=self.phone_number).show()

                    # to fix circular dependency
                    from apps.dhis.ussd.screen import SectionScreen
                    # all sections are not visited so show section screen
                    return SectionScreen(session_id=self.session_id, phone_number=self.phone_number).show()
        return self.ussd_end("No data sets are found")

    def prev(self):
        pass
