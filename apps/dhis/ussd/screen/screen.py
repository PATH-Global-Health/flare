from enum import IntEnum

from django.http import HttpResponse
from django.conf import settings

from ..store.store import Store


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
            'data_element': '',
            'category_option_combo': '',
            'period': '',
            'dataset': '',
            'section': '',
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
