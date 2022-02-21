from decouple import config

from apps.dhis.ussd.screen.screen import Screen, Level
from apps.dhis.ussd.screen.section_screen import SectionScreen
from apps.dhis.ussd.store.store import Store
from apps.dhis.utils import generate_period, get_period


class PeriodScreen(Screen):
    """displays the period based on the period type of the data set"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.PERIODS)

    def show(self):
        periods = generate_period(self.state['period_type'], self.state['open_future_periods'],
                                  config('PAGINATION_LIMIT', 3), self.state['begin_period'], self.state['direction'],
                                  self.state['direction_change'])
        menu_text = "Period:\n"
        menu_text += "+. Next\n"

        for key, value in periods[1].items():
            menu_text += "{}. {}\n".format(key, value["display"])

        menu_text += "-. Prev"

        return self.ussd_proceed(menu_text)

    def validate(self):
        periods = generate_period(self.state['period_type'], self.state['open_future_periods'],
                                  config('PAGINATION_LIMIT', 3), self.state['begin_period'], self.state['direction'],
                                  self.state['direction_change'])

        if self.user_response == '+' or self.user_response == '-':
            self.state['begin_period'] = periods[0]
            # this state is required to fix a one week discrepancy when user presses + and then - or vice versa
            self.state['direction_change'] = True if self.user_response != self.state['direction'] else False
            self.state['direction'] = self.user_response
            self.save()
            return False

        if self.user_response in periods[1].keys():
            self.state['begin_period'] = periods[0]
            # this is the period. The data is structured in such as way
            # {
            #     1: {'period': '202050', display:"W50 - 2020-12-07 - 2020-12-13"},
            #     2: {...}
            # }
            self.state['period'] = get_period(periods[1][self.user_response]['period'])
            self.save()
            return True

        return False

    def next(self):
        return SectionScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        pass
