import datetime
import random

from epiweeks import Week, Year

from apps.dhis.models import DHIS2User, OrgUnit, DatasetDataElement, DataElement
from apps.dhis.ussd.screen import Level

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
def generate_week_periods(open_future_periods, page_limit, begin_period, direction, direction_change):
    weeks_to_display = {}

    # When the user first visits the period screen the begin_period variable is empty.
    # Therefore, use the current week as default.
    week = Week.thisweek("iso") + open_future_periods

    # If begin_period variable has a date, use it to calculate the weeks to display.
    if begin_period != '':
        week = Week.fromdate(datetime.datetime.strptime(begin_period, '%Y-%m-%d'), 'iso')
        # This logic is to fix week discrepancy when a user clicks + and changes the direction and press - or vice versa
        if direction_change:
            if direction == '+':
                week += page_limit - 1
            if direction == '-':
                week -= page_limit - 1

    # We should not open future dates for data entry. The -1 is to prevent from opening this week.
    if direction == '+' and week + page_limit > Week.thisweek("iso") + open_future_periods:
        week = Week.thisweek("iso") + open_future_periods - page_limit - 1

    rng = range(page_limit, 0, -1) if direction == '+' else range(page_limit)

    for key, i in enumerate(rng):
        w = week + i if direction == '+' else week - (i + 1)
        weeks_to_display[str(key + 1)] = {
            "period": w.isoformat(),
            "display": "W{} - {} - {}".format(w.weektuple()[1], w.startdate(), w.enddate())
        }

        # Take the first week to calculate the beginning period in the next screen.
        if direction == '+' and i == page_limit:
            begin_period = str(w.enddate())
        # Take the final week to calculate the beginning week in the next screen.
        if direction == '-' and i == page_limit - 1:
            begin_period = str(w.startdate())

    return begin_period, weeks_to_display


def generate_period(period_type, open_future_periods, page_limit, begin_period='', direction='-',
                    direction_change=False):
    if period_type == "Weekly":
        return generate_week_periods(open_future_periods, page_limit, begin_period, direction, direction_change)

    return {}


def validate_number(value):
    if value is not None and value.isnumberic():
        return True, value
    return False, value


def validate_integer(value):
    if value is not None and value.isdigit():
        return True, int(value)
    return False, value


def validate_int_positive(value):
    val = validate_integer(value)
    if val[0] and val[1] > 0:
        return True, val[1]

    return False, value


def validate_int_zero_or_positive(value):
    val = validate_integer(value)
    if val[0] and val[1] >= 0:
        return True, val[1]

    return False, value


def validate_int_negative(value):
    val = validate_integer(value)
    if val[0] and val[1] < 0:
        return True, val[1]

    return False, value


def validate_text(value):
    if value is not None:
        return True, value
    return False, value


def validate_data_element_by_value_type(value_type, value):
    if value_type == "NUMBER":
        return validate_number(value)

    if value_type == "INTEGER":
        return validate_integer(value)

    if value_type == "INTEGER_POSITIVE":
        return validate_positive_integer(value)

    if value_type == "INTEGER_ZERO_OR_POSITIVE":
        return validate_int_zero_or_positive(value)

    if value_type == "INTEGER_NEGATIVE":
        return validate_int_negative(value)

    if value_type == "TEXT" or value_type == "LONG_TEXT":
        return validate_text(value)


def get_screen(session_id, phone_number, user_response, level):
    if level == Level.LOGIN:
        from apps.dhis.ussd.screen import LoginScreen
        return LoginScreen(session_id=session_id, phone_number=phone_number,
                           user_response=user_response)
    elif level == Level.RESTORE:
        from apps.dhis.ussd.screen import RestoreSessionScreen
        return RestoreSessionScreen(session_id=session_id, phone_number=phone_number,
                                    user_response=user_response)
    elif level == Level.ORG_UNITS:
        from apps.dhis.ussd.screen import OrgUnitScreen
        return OrgUnitScreen(session_id=session_id, phone_number=phone_number,
                             user_response=user_response)
    elif level == Level.DATASETS:
        from apps.dhis.ussd.screen import DatasetScreen
        return DatasetScreen(session_id=session_id, phone_number=phone_number,
                             user_response=user_response)
    elif level == Level.SECTIONS:
        from apps.dhis.ussd.screen import SectionScreen
        return SectionScreen(session_id=session_id, phone_number=phone_number,
                             user_response=user_response)
    elif level == Level.PERIODS:
        from apps.dhis.ussd.screen import PeriodScreen
        return PeriodScreen(session_id=session_id, phone_number=phone_number,
                            user_response=user_response)
    elif level == Level.DATA_ELEMENTS:
        from apps.dhis.ussd.screen import DataElementScreen
        return DataElementScreen(session_id=session_id, phone_number=phone_number,
                                 user_response=user_response)
    elif level == Level.SAVE_OPTIONS:
        from apps.dhis.ussd.screen import SaveOptionsScreen
        return SaveOptionsScreen(session_id=session_id, phone_number=phone_number,
                                 user_response=user_response)


def is_data_element_compulsory(compulsory_data_elements, data_element):
    for de in compulsory_data_elements:
        if data_element.data_element_id == de['id']:
            return True
    return False

def store_data_elements_assigned_2_dataset(ds, dataset, version, dhis2_instance):
    for data_element in dataset['dataSetElements']:
        de = DataElement.objects.get_or_none(data_element_id=data_element['dataElement']['id'])
        if de is not None:

            for coc in de.category_combo.categoryoptioncombo_set.all():
                ds_de = DatasetDataElement.objects.get_or_none(data_set__dataset_id=ds.dataset_id,
                                                               data_element__data_element_id=de.data_element_id,
                                                               category_option_combo__category_option_combo_id=coc.category_option_combo_id)
                if ds_de is None:
                    ds_de = DatasetDataElement()
                ds_de.data_element = de
                ds_de.category_option_combo = coc
                ds_de.data_set = ds

                if 'compulsoryDataElementOperands' in dataset:
                    ds_de.compulsory = is_data_element_compulsory(dataset['compulsoryDataElementOperands'], de)

                ds_de.version = version
                ds_de.instance = dhis2_instance
                ds_de.save()

    DatasetDataElement.objects.exclude(version=version).delete()

def store_org_units_assigned_2_dataset(ds, org_units):
    for org_unit in org_units:
        ou = OrgUnit.objects.get_or_none(org_unit_id=org_unit['id'])
        if ou is not None:
            ds.org_units.add(ou)
    ds.save()

def format_dataset_with_section(sections):
    dataset_sections = {}
    for i, section in enumerate(sections):
        dataset_sections[i + 1] = {'name': section.name, 'id': section.section_id, 'data_elements': []}
        for ds_de in section.datasetdataelement_set.all().order_by('sort_order'):
            dataset_sections[i + 1]['data_elements'].append(
                {
                    'data_element_name': ds_de.data_element.name,
                    'data_element_id': ds_de.data_element.data_element_id,
                    'category_option_combo_name': ds_de.category_option_combo.name,
                    'category_option_combo_id': ds_de.category_option_combo.category_option_combo_id,
                    'data_element_value_type': ds_de.data_element.value_type
                }
            )

    return dataset_sections

def format_dataset_with_out_section(dataset):
    data_elements = []
    for ds_de in dataset.datasetdataelement_set.all():
        data_elements.append(
            {
                'data_element_name': ds_de.data_element.name,
                'data_element_id': ds_de.data_element.data_element_id,
                'category_option_combo_name': ds_de.category_option_combo.name,
                'category_option_combo_id': ds_de.category_option_combo.category_option_combo_id,
                'data_element_value_type': ds_de.data_element.value_type
            }
        )
    return data_elements