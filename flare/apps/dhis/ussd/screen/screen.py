from enum import IntEnum

from django.http import HttpResponse

from apps.dhis.ussd.store import Store


class Level(IntEnum):
    LOGIN = 1
    RESTORE = 2
    ORG_UNITS = 3
    DATASETS = 4
    PERIODS = 5
    SECTIONS = 6
    SECTION_FORM = 7
    DEFAULT_FORM=8
    SAVE_OPTIONS = 9  # complete and incomplete


class Screen(object):
    def __init__(self, session_id, phone_number=None, user_response=None, level=Level.LOGIN):
        self.session_id = session_id
        self.phone_number = phone_number
        self.user_response = user_response
        self.level = level
        self.state = {
            'passcode': '', # The password that the user entered to access the DHIS2 form.
            'level': Level.LOGIN, # The screen that is currently visible to the user.
            'org_unit': '', # Org unit selected
            'period': '', # The period in EpiWeek that the user selected.
            'dataset': '', # The dataset id selected
            'period_type': '', # The period type i.e. week, month ...
            'open_future_periods': '',# Shows the number of days, weeks, months... in the future the program should open
            'has_section': '', # Boolean value to indicate if the selected dataset has section or not
            'section': '', # The section index that is selected by the user
            'begin_period': '', # Used in the period screen. The first period to start generating periods.
            'direction': '-', # Used in the period screen. The default option is - so that users will see past periods.
            'direction_change': False, # This is used in the period screen. The user had been pressing the - option but had now begun to press the + option.
            'data_element_index': 0, # The index of the currently displayed data element to the user.
            'data_element_values': {}, #{data_element_id|category_combo_option_id : value}
            'sections_visited': [] # Index of the sections that the user visited.
        }

        if Store.exists(self.session_id):
            self.state = Store.get(self.session_id)

    def show(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def prev(self):
        raise NotImplementedError

    def ussd_proceed(self, display_text):
        self.save()
        display_text = "CON {}".format(display_text)

        return HttpResponse(display_text)

    def ussd_end(self, display_text):
        Store.delete(self.session_id)
        Store.delete(key="usr_state_{}".format(self.state['passcode']))
        display_text = "END {}".format(display_text)

        return HttpResponse(display_text)

    def save(self, level=None):
        self.state['level'] = self.level if level is None else level
        Store.set(self.session_id, self.state)
