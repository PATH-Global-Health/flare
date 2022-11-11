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
            'passcode': '',
            'level': Level.LOGIN,
            'org_unit': '',
            'period': '',
            'dataset': '',
            'period_type': '',
            'open_future_periods': '',
            'has_section': '',
            'section': '',
            'begin_period': '',
            'direction': '-',
            'direction_change': False,
            'data_element_index': 0,
            'data_element_values': {},
            'sections_visited': []
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
