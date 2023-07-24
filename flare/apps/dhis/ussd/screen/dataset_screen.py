from apps.dhis.ussd.screen import Screen, Level, PeriodScreen
from apps.dhis.ussd.store import Store


class DatasetScreen(Screen):
    """displays the dataset that is assigned to the selected org unit"""

    def __init__(self, session_id, phone_number, user_response=None):
        super().__init__(session_id, phone_number, user_response, Level.DATASETS)
        self.datasets = None
        dataset_key = "ou_{}".format(self.state['org_unit'])

        if Store.exists(dataset_key):
            self.datasets = Store.get(dataset_key)

    def generate_menu_item(self):
        for key, value in self.datasets.items():
            self.menu_items.append("{}. {}".format(key, value['name']))

    def show(self):
        if self.datasets:
            self.generate_menu_item()
            paginated_menu = self.paginate_menu_item(self.user_response)
            # Add a menu title at the beginning of the menu options
            paginated_menu.insert(0, "Dataset:")
            # Add back option at the end
            paginated_menu.append("#. Back")

            return self.ussd_proceed("\n".join(paginated_menu))

        return self.ussd_end("No data set found.")

    def validate(self):
        if self.datasets:
            if self.user_response in self.datasets.keys():
                self.state['dataset'] = self.datasets[self.user_response]['id']
                self.state['period_type'] = self.datasets[self.user_response]['period_type']
                self.state['open_future_periods'] = self.datasets[self.user_response]['open_future_periods']
                self.state['has_section'] = self.datasets[self.user_response]['has_section']
                self.save()
                return True

        return False

    def next(self):
        return PeriodScreen(session_id=self.session_id, phone_number=self.phone_number).show()

    def prev(self):
        from apps.dhis.ussd.screen import OrgUnitScreen
        return OrgUnitScreen(session_id=self.session_id, phone_number=self.phone_number).show()
