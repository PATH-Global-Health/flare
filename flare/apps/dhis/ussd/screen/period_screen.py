import os

from apps.dhis.ussd.screen import Screen, Level
from apps.dhis.ussd.store import Store
from apps.dhis.utils import generate_period


class PeriodScreen(Screen):
    """displays the period based on the period type of the data set"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.PERIODS)

    def show(self):
        periods = generate_period(self.state['period_type'], self.state['open_future_periods'],
                                  self.menu_items_size, self.state['begin_period'], self.user_response)
        menu_text = "Period:\n"

        for key, value in periods[1].items():
            menu_text += "{}. {}\n".format(key, value["display"])

        menu_text += "+. Next -. Prev \n"
        menu_text += "#. Back"

        self.state['begin_period'] = periods[0]
        self.save()

        return self.ussd_proceed(menu_text)

    def validate(self):
        periods = generate_period(self.state['period_type'], self.state['open_future_periods'],
                                  self.menu_items_size, self.state['begin_period'])

        print('begin_period = {}'.format(periods[0]))
        if self.user_response == '+' or self.user_response == '-':
            return False

        if self.user_response in periods[1].keys():
            self.state['period'] = periods[1][self.user_response]['period']
            self.save()
            return True

        return False

    def next(self):
        from apps.dhis.ussd.screen import FormTypeScreen
        return FormTypeScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        from apps.dhis.ussd.screen import DatasetScreen
        return DatasetScreen(session_id=self.session_id, phone_number=self.phone_number).show()
