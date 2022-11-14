from apps.dhis.ussd.screen import Screen, Level, PeriodScreen
from apps.dhis.ussd.store import Store


class DatasetScreen(Screen):
    """displays the dataset that is assigned to the selected org unit"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.DATASETS)

    def show(self):
        key = "ou_{}".format(self.state['org_unit'])
        if Store.exists(key):
            datasets = Store.get(key)
            menu_text = "Dataset:\n"
            for key, value in datasets.items():
                menu_text += "{}. {}\n".format(key, value['name'])

            return self.ussd_proceed(menu_text)

        return self.ussd_end("No data set found.")

    def validate(self):
        key = "ou_{}".format(self.state['org_unit'])
        if Store.exists(key):
            datasets = Store.get(key)
            if self.user_response in datasets.keys():
                self.state['dataset'] = datasets[self.user_response]['id']
                self.state['period_type'] = datasets[self.user_response]['period_type']
                self.state['open_future_periods'] = datasets[self.user_response]['open_future_periods']
                self.state['has_section'] = datasets[self.user_response]['has_section']
                self.save()
                return True

        return False

    def next(self):
        return PeriodScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        pass
