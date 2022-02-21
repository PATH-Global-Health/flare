import datetime
import random

from epiweeks import Week, Year

from apps.dhis.models import DHIS2User

CHARACTERS = "abcdefghijkmnpqrtuvwxyz2345689"
LENGTH = 6


def generate_passcode():
    password = ""
    for i in range(LENGTH):
        password += random.choice(CHARACTERS)
    return password


def unique_passcode():
    passcode = generate_passcode()
    user = DHIS2User.objects.get_or_none(passcode=passcode)
    n = 593775  # combination - 𝐶(30,6) 30 unique characters and passcode length is 6
    i = 0
    while i <= n and user is not None:
        i += 1
        passcode = generate_passcode()
        user = DHIS2User.objects.get_or_none(passcode=passcode)
    if i > n:
        return "No unique passcode"
    return passcode


# This function generates week period for dhis2
# The data return data is structured in such as way
#          ("2020-12-07", {
#             1: {'period': '202050', 'display':"W50 - 2020-12-07 - 2020-12-13"},
#             2: {...}
#         })
# The first value in the tuple is used as begin period and the second value is list of periods
# to display. The amount of periods generated depends on the value set for PAGINATION_LIMIT in .env file.
def generate_week_periods(open_future_periods, pagination_limit, begin_period, direction, direction_change):
    weeks_to_display = {}
    page_limit = int(pagination_limit)

    # When the user first visits the period screen the begin_period variable is empty.
    # Therefore, use the current week as default.
    week = Week.thisweek("iso") + open_future_periods

    # If begin_period variable has a date, use it to calculate the weeks to display.
    if begin_period != '':
        week = Week.fromdate(datetime.datetime.strptime(begin_period, '%Y-%m-%d'), 'iso')
        # This logic to fix the one week discrepancy when a user clicks + and changes the direction and press -
        if direction_change:
            if direction == '+':
                week += 1
            if direction == '-':
                week -= 1

    # We should not open future dates for data entry. The -1 is to prevent from opening this week.
    if direction == '+' and week + page_limit > Week.thisweek("iso") + open_future_periods:
        week = Week.thisweek("iso") + open_future_periods - page_limit - 1

    rng = range(page_limit, 0, -1) if direction == '+' else range(page_limit)

    for key, i in enumerate(rng):
        w = week + i if direction == '+' else week - (i + 1)
        weeks_to_display[str(key + 1)] = {
            "period": w.cdcformat(),
            "display": "W{} - {} - {}".format(w.weektuple()[1], w.startdate(), w.enddate())
        }

        # Take the first week to calculate the beginning period in the next screen.
        if direction == '+' and i == page_limit:
            begin_period = str(w.enddate())
        # Take the final week to calculate the beginning week in the next screen.
        if direction == '-' and i == page_limit - 1:
            begin_period = str(w.startdate())

    return begin_period, weeks_to_display


def generate_period(period_type, open_future_periods, pagination_limit, begin_period='', direction='-',
                    direction_change=False):
    if period_type == "Weekly":
        return generate_week_periods(open_future_periods, pagination_limit, begin_period, direction, direction_change)

    return {}
