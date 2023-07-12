import os
from enum import IntEnum

from django.http import HttpResponse

from apps.dhis.ussd.store import Store


class Level(IntEnum):
    LOGIN = 1
    RESTORE = 2
    ORG_UNITS = 3
    DATASETS = 4
    PERIODS = 5
    FORM_TYPES = 6
    SECTIONS = 7  # 6
    SECTION_FORM = 8  # 7
    DEFAULT_FORM = 9  # 8
    GROUPS = 10  # 9
    GROUP_FORM = 11  # 10
    SAVE_OPTIONS = 12  # complete and incomplete


class Screen(object):
    def __init__(self, session_id, phone_number=None, user_response=None, level=Level.LOGIN):
        self.session_id = session_id
        self.phone_number = phone_number
        self.user_response = user_response
        self.level = level
        # The size of the menu items to display in a screen
        self.menu_items_size = int(os.getenv('MENU_ITEMS_SIZE', 2))
        # Lists all the menu items available on a particular screen
        self.menu_items = []

        self.state = {
            # The password that the user entered to access the DHIS2 form.
            'passcode': '',
            # The screen that is currently visible to the user.
            'level': Level.LOGIN,
            'org_unit': '',  # Org unit ID selected
            'period': '',  # The period in EpiWeek that the user selected.
            'dataset': '',  # The dataset id selected
            'period_type': '',  # The period type i.e. Weekly, Monthly ...
            # Shows the number of days, weeks, months... in the future the program should open
            'open_future_periods': '',
            'has_section': '',  # Boolean value to indicate if the selected dataset has section or not
            'section': '',  # The section index that is selected by the user
            'group': '',  # The group index that is selected by the user
            # Used in the period screen. The first period to start generating periods.
            'begin_period': '',
            # Used in the period screen. The default option is - so that users will see past periods.
            'direction': '-',
            # This is used in the period screen. The user had been pressing the - option but had now begun to press the + option.
            'direction_change': False,
            # Slides through the content list to generate paginated menu
            'slide_window_start': 0,  # Index of the first menu item
            'slide_window_end': self.menu_items_size,  # Index of the last menu item
            # The index of the currently displayed data element to the user.
            'data_element_index': 0,
            'data_element_values': {},  # {data_element_id-category_option_combo_id : value}
            # Index of the sections that the user visited.
            'sections_visited': [],
            # Index of the groups that the user visited.
            'groups_visited': []
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

    def generate_menu_item(self):
        raise NotImplementedError

    def paginate_menu_item(self, direction=''):
        start = int(self.state['slide_window_start'])
        end = int(self.state['slide_window_end'])
        paginated_menu_items = []
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(self.menu_items)
        print('start = {}'.format(start))
        print('end = {}'.format(end))
        print('menu_items_size = {}'.format(self.menu_items_size))

        if direction == '-':
            self.state['slide_window_start'] = start - \
                self.menu_items_size if start - self.menu_items_size >= 0 else start
            self.state['slide_window_end'] = end - \
                self.menu_items_size if end - self.menu_items_size >= self.menu_items_size else end
        elif direction == '+':
            # If we want to display 3 menu items per screen and the size of menu_items is 41,
            # then we need to calculate the minimum and maximum upper boundaries for displaying the menu items.
            # Based on this, we can set the min_upper_boundary to 39 and the max_upper_boundary to 42.
            # 42 = ((41/3) + (1 if 41 % 3 > 0 else 0)) * 3
            max_upper_boundary = (int(len(
                self.menu_items) / self.menu_items_size) + 1 if len(self.menu_items) % self.menu_items_size > 0 else 0) * self.menu_items_size
            min_upper_boundary = max_upper_boundary - self.menu_items_size

            self.state['slide_window_start'] = start + self.menu_items_size if start + \
                self.menu_items_size <= min_upper_boundary else start
            self.state['slide_window_end'] = end + \
                self.menu_items_size if end + \
                self.menu_items_size <= max_upper_boundary else end

        print("self.state['slide_window_start'] = {}".format(
            self.state['slide_window_start']))
        print("self.state['slide_window_end'] = {}".format(
            self.state['slide_window_end']))

        if len(self.menu_items) > 0:
            print(
                self.menu_items[self.state['slide_window_start']:self.state['slide_window_end']])
            paginated_menu_items = self.menu_items[self.state['slide_window_start']                                                   :self.state['slide_window_end']]

        # A pagination menu is necessary when there are more menu items than can be displayed on a single screen.
        if len(self.menu_items) > self.menu_items_size:
            paginated_menu_items.append('+. Next -. Prev')

        Store.set(self.session_id, self.state)

        return paginated_menu_items

    def reset_state(self):
        self.state['slide_window_start'] = 0
        self.state['slide_window_end'] = 2
        Store.set(self.session_id, self.state)

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
