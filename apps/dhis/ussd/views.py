from apps.dhis.ussd.screen import Screen, Level


class USSDView:

    def __init__(self, session_id, phone_number, user_response=None):
        self.session_id = session_id
        self.phone_number = phone_number
        self.user_response = user_response
        self.screen = Screen(session_id=self.session_id, phone_number=self.phone_number)

    def __show_initial(self):
        from apps.dhis.ussd.screen import LoginScreen
        screen = LoginScreen(session_id=self.session_id, phone_number=self.phone_number)
        return screen.show()

    def show(self):
        if self.user_response == "":
            return self.__show_initial()

        if self.screen.state['level'] == Level.LOGIN:
            from apps.dhis.ussd.screen import LoginScreen
            self.screen = LoginScreen(session_id=self.session_id, phone_number=self.phone_number,
                                      user_response=self.user_response)
        elif self.screen.state['level'] == Level.ORG_UNITS:
            from apps.dhis.ussd.screen import OrgUnitScreen
            self.screen = OrgUnitScreen(session_id=self.session_id, phone_number=self.phone_number,
                                        user_response=self.user_response)
        elif self.screen.state['level'] == Level.DATASETS:
            from apps.dhis.ussd.screen import DatasetScreen
            self.screen = DatasetScreen(session_id=self.session_id, phone_number=self.phone_number,
                                        user_response=self.user_response)
        elif self.screen.state['level'] == Level.SECTIONS:
            from apps.dhis.ussd.screen import SectionScreen
            self.screen = SectionScreen(session_id=self.session_id, phone_number=self.phone_number,
                                        user_response=self.user_response)
        elif self.screen.state['level'] == Level.PERIODS:
            from apps.dhis.ussd.screen import PeriodScreen
            self.screen = PeriodScreen(session_id=self.session_id, phone_number=self.phone_number,
                                       user_response=self.user_response)
        elif self.screen.state['level'] == Level.DATA_ELEMENTS:
            from apps.dhis.ussd.screen import DataElementScreen
            self.screen = DataElementScreen(session_id=self.session_id, phone_number=self.phone_number,
                                            user_response=self.user_response)
        elif self.screen.state['level'] == Level.SAVE_OPTIONS:
            from apps.dhis.ussd.screen import SaveOptionsScreen
            self.screen = SaveOptionsScreen(session_id=self.session_id, phone_number=self.phone_number,
                                            user_response=self.user_response)

        if not self.screen.validate():
            return self.screen.show()
        else:
            return self.screen.next()
