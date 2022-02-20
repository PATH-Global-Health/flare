from apps.dhis.ussd.screen.screen import Screen, Level
from apps.dhis.ussd.screen.login_screen import LoginScreen
from apps.dhis.ussd.screen.org_unit_screen import OrgUnitScreen
from apps.dhis.ussd.screen.dataset_screen import DatasetScreen
from apps.dhis.ussd.screen.section_screen import SectionScreen
from apps.dhis.ussd.screen.period_screen import PeriodScreen


class USSDView:

    def __init__(self, session_id, phone_number, user_response=None):
        self.session_id = session_id
        self.phone_number = phone_number
        self.user_response = user_response
        self.screen = Screen(session_id=self.session_id, phone_number=self.phone_number)

    def __show_initial(self):
        screen = LoginScreen(session_id=self.session_id, phone_number=self.phone_number)
        return screen.show()

    def show(self):
        if self.user_response == "":
            return self.__show_initial()

        if self.screen.state['level'] == Level.LOGIN:
            self.screen = LoginScreen(session_id=self.session_id, phone_number=self.phone_number,
                                      user_response=self.user_response)
        elif self.screen.state['level'] == Level.ORG_UNITS:
            self.screen = OrgUnitScreen(session_id=self.session_id, phone_number=self.phone_number,
                                        user_response=self.user_response)
        elif self.screen.state['level'] == Level.DATASETS:
            self.screen = DatasetScreen(session_id=self.session_id, phone_number=self.phone_number,
                                        user_response=self.user_response)
        elif self.screen.state['level'] == Level.SECTIONS:
            self.screen = SectionScreen(session_id=self.session_id, phone_number=self.phone_number,
                                        user_response=self.user_response)
        elif self.screen.state['level'] == Level.PERIODS:
            self.screen = PeriodScreen(session_id=self.session_id, phone_number=self.phone_number,
                                       user_response=self.user_response)

        if not self.screen.validate():
            return self.screen.show()
        else:
            return self.screen.next()
