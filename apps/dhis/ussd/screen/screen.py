from enum import IntEnum

from django.http import HttpResponse

from apps.dhis.ussd.store.store import Store


class Level(IntEnum):
    LOGIN = 1
    ORG_UNITS = 2
    DATASETS = 3
    PERIODS = 4
    SECTIONS = 5
    DATA_ELEMENTS = 6
    SAVE_OPTIONS = 7  # complete and incomplete


class Screen(object):
    def __init__(self, session_id, phone_number=None, user_response=None, level=None):
        self.session_id = session_id
        self.phone_number = phone_number
        self.user_response = user_response
        self.level = level
        self.state = {
            'passcode': '',
            'level': '',
            'org_unit': '',
            'period': '',
            'dataset': '',
            'period_type': '',
            'open_future_periods': '',
            'section': '',
            'begin_period': '',
            'direction': '-',
            'direction_change': False,
            'data_element_index': -1,
            'previous_data_element_value_error': False,
            'data_element_values': {}
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
        display_text = "END {}".format(display_text)

        return HttpResponse(display_text)

    def save(self):
        self.state['level'] = self.level
        Store.set(self.session_id, self.state)
