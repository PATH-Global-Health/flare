from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store
from apps.dhis.utils import validate_data_element_by_value_type
from apps.dhis.tasks import save_values_to_database, save_values_to_database_batch


class SectionFormScreen(Screen):
    """displays the data elements in the selected section"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.SECTION_FORM)
        dataset_key = "ds_{}".format(self.state['dataset'])
        self.dataset = None

        if Store.exists(dataset_key):
            self.dataset = Store.get(dataset_key)

            if self.state['section'] in self.dataset.keys():
                self.data_elements = self.dataset[self.state['section']
                                                  ]['data_elements']
                self.data_element_index = int(self.state['data_element_index'])
                self.data_element_value_type = self.data_elements[
                    self.data_element_index]['data_element_value_type']
                self.data_element = self.data_elements[self.data_element_index]['data_element_id']
                self.category_option_combo = self.data_elements[
                    self.data_element_index]['category_option_combo_id']

    def show(self):
        if self.dataset:
            if self.data_element_index < len(self.data_elements):
                # If the category option combination name is not default, then append it to the data element
                # name

                data_element_name = self.data_elements[self.data_element_index]['data_element_name']
                menu_text = " * {}".format(
                    data_element_name) if self.get_compulsory() else data_element_name

                cat_opt_combo_name = self.data_elements[self.data_element_index]['category_option_combo_name']
                menu_text += " - {}".format(
                    cat_opt_combo_name) if cat_opt_combo_name != 'default' else ""
                # If the key (data element id and cat opt combo id) is within the data element values dictionary and
                # the value is not empty, display the value to the user.

                key = self.get_key()
                skip_menu_added = False

                if key in self.state['data_values']:
                    if self.state['data_values'][key]:
                        menu_text += " - [{}]".format(
                            self.state['data_values'][key])
                    skip_menu_added = True  # we already added a skip menu
                    # user can skip modifying the value previously entered.
                    menu_text += "\n*. Skip"

                # if no skip menu is added and the data element is not compulsory, add the skip menu
                if not skip_menu_added and not self.get_compulsory():
                    menu_text += "\n*. Skip"
                menu_text += "\n#. Back"

                return self.ussd_proceed(menu_text)
            else:
                self.next()

        return self.ussd_end("No data sets found")

    # validate will always return false until all data elements are filled
    def validate(self):
        if self.dataset:
            # if the current section selected is not in the section visited list, add it
            if self.state['section'] not in self.state['sections_visited']:
                self.state['sections_visited'].append(self.state['section'])

            # if the data element is not compulsory and the user entered *, skip it.
            if self.user_response == '*' and not self.get_compulsory():
                return True

            key = self.get_key()

            # If the user entered * to skip entering a value and there is a previously entered data value, return true.
            # This is useful when editing data because it allows you to skip through data elements and only enter values
            # for those that need to be edited.
            if self.user_response == '*' and key in self.state['data_values']:
                return True

            # validate the data element
            result = validate_data_element_by_value_type(
                self.get_compulsory(), self.data_element_value_type, self.user_response)

            if result[0]:
                # save the value that is received from the user in the state. The key is a concatenation of
                # data element and category option combo ids.

                self.state['data_values'][key] = result[1]
                self.save()

                # Save into database
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
                # reset the data element index
                self.state['data_element_index'] = 0

                # If all sections are visited, show the save options screen
                if len(self.dataset.keys()) == len(self.state['sections_visited']):
                    from apps.dhis.ussd.screen import SaveOptionsScreen
                    return SaveOptionsScreen(session_id=self.session_id, phone_number=self.phone_number).show()

                # to fix circular dependency
                from apps.dhis.ussd.screen import SectionScreen
                # all sections are not visited so show section screen
                return SectionScreen(session_id=self.session_id, phone_number=self.phone_number).show()
        return self.ussd_end("No datasets are found")

    def prev(self):
        self.data_element_index -= 1

        if self.data_element_index < 0:
            # We've shown the first data element, so return to the section screen.
            from apps.dhis.ussd.screen import SectionScreen
            return SectionScreen(session_id=self.session_id, phone_number=self.phone_number).show()
        else:
            self.state['data_element_index'] = self.data_element_index
            self.save()
            return self.show()

    def get_key(self):
        # The key is generated in order to temporarily store the value in redis.
        data_element = self.data_elements[self.data_element_index]['data_element_id']
        category_option_combo = self.data_elements[self.data_element_index]['category_option_combo_id']
        return "{}-{}".format(data_element, category_option_combo)

    def get_compulsory(self):
        return self.data_elements[self.data_element_index]['compulsory']
