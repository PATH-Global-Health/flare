import datetime
import random
import logging

from epiweeks import Week, Year
from dhis2 import Api, RequestException

from apps.dhis.models import DHIS2User, OrgUnit, DatasetDataElement, DataElement, \
    DataValueSet, Dataset, CategoryOptionCombo, DataValue
from apps.dhis.ussd.screen import Level


CHARACTERS = "abcdefghijkmnpqrtuvwxyz2345689"
LENGTH = 6

logger = logging.getLogger(__name__)


def generate_passcode():
    password = ""
    for i in range(LENGTH):
        password += random.choice(CHARACTERS)
    return password


def unique_passcode():
    passcode = generate_passcode()
    user = DHIS2User.objects.get_or_none(passcode=passcode)
    # combination - 𝐶(30,6) 30 unique characters and passcode length is 6
    n = 593775
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
# to display. The amount of periods generated depends on the value set for MENU_ITEM_SIZE in .env file.
def generate_week_periods(open_future_periods, menu_item_size, begin_period, direction):
    weeks_to_display = {}

    # When the user first visits the period screen the begin_period variable is empty.
    # Therefore, use the current week as default.
    week = Week.thisweek("iso") + open_future_periods - 1

    # If begin_period variable has a date, use it to calculate the weeks to display.
    if begin_period != '':
        week = Week.fromdate(datetime.datetime.strptime(
            begin_period, '%Y-%m-%d'), 'iso')

    # We should not open future dates for data entry. The -1 is to prevent from opening this week.
    if direction == '+' and week + menu_item_size > Week.thisweek("iso") + open_future_periods - 1:
        week = Week.thisweek("iso") + open_future_periods - menu_item_size - 1

    # To generate a list of weeks for the user, it's necessary to adjust the start of the week in
    # order to obtain a range of weeks with the desired page limit. This can be achieved by either
    # adding or subtracting from the start of the week.
    if direction == '+':
        week += menu_item_size
    elif direction == '-':
        week -= menu_item_size

    # begin period will be retrieved and saved in the Redis cache for future reference in this function
    begin_period = str(week.startdate())

    # generate menu items
    for key, i in enumerate(range(menu_item_size)):
        w = week - i
        weeks_to_display[str(key + 1)] = {
            "period": w.isoformat(),
            "display": "W{} - {}".format(w.weektuple()[1], w.startdate())
            # "display": "W{} - {} - {}".format(w.weektuple()[1], w.startdate(), w.enddate())
        }

    return begin_period, weeks_to_display


def generate_period(period_type, open_future_periods, menu_item_size, begin_period='', direction=''):
    if period_type == "Weekly":
        return generate_week_periods(open_future_periods, menu_item_size, begin_period, direction)

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


def validate_data_element_by_value_type(compulsory, value_type, value):
    if compulsory or len(value) > 0:
        # Check the data type of a value if the data element is compulsory or if the user enters data even if the
        # data element is optional.
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
    # The data element is not compulsory so we don't need to validate the data type.
    # Just return true with empty value.
    return True, ""


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
    elif level == Level.SECTION_FORM:
        from apps.dhis.ussd.screen import SectionFormScreen
        return SectionFormScreen(session_id=session_id, phone_number=phone_number,
                                 user_response=user_response)
    elif level == Level.DEFAULT_FORM:
        from apps.dhis.ussd.screen import DefaultFormScreen
        return DefaultFormScreen(session_id=session_id, phone_number=phone_number,
                                 user_response=user_response)
    elif level == Level.FORM_TYPES:
        from apps.dhis.ussd.screen import FormTypeScreen
        return FormTypeScreen(session_id=session_id, phone_number=phone_number,
                              user_response=user_response)
    elif level == Level.GROUPS:
        from apps.dhis.ussd.screen import GroupScreen
        return GroupScreen(session_id=session_id, phone_number=phone_number,
                           user_response=user_response)
    elif level == Level.GROUP_FORM:
        from apps.dhis.ussd.screen import GroupFormScreen
        return GroupFormScreen(session_id=session_id, phone_number=phone_number,
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
        de = DataElement.objects.get_or_none(
            data_element_id=data_element['dataElement']['id'])
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
                    ds_de.compulsory = is_data_element_compulsory(
                        dataset['compulsoryDataElementOperands'], de)

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


def store_data_elements_assigned_2_data_element_group(deg, data_elements):
    for data_element in data_elements:
        de = DataElement.objects.get_or_none(
            data_element_id=data_element['id'])
        if de is not None:
            deg.data_element.add(de)
    deg.save()


def format_dataset_with_section(sections):
    dataset_sections = {}
    for i, section in enumerate(sections):
        dataset_sections[i + 1] = {'name': section.name,
                                   'id': section.section_id, 'data_elements': []}
        for ds_de in section.datasetdataelement_set.all().order_by('sort_order'):
            dataset_sections[i + 1]['data_elements'].append(
                {
                    'data_element_name': ds_de.data_element.name,
                    'data_element_id': ds_de.data_element.data_element_id,
                    'category_option_combo_name': ds_de.category_option_combo.name,
                    'category_option_combo_id': ds_de.category_option_combo.category_option_combo_id,
                    'data_element_value_type': ds_de.data_element.value_type,
                    'compulsory': ds_de.compulsory,
                    'initialize_with_zero': ds_de.initialize_with_zero
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
                'data_element_value_type': ds_de.data_element.value_type,
                'compulsory': ds_de.compulsory,
                'initialize_with_zero': ds_de.initialize_with_zero
            }
        )
    return data_elements


def in_groupset(data_element_group, data_element_groupsets):
    is_deg_belongs_2_degs = False
    if 'groupSets' in data_element_group:
        for groupset in data_element_group['groupSets']:
            if groupset['id'] in data_element_groupsets:
                is_deg_belongs_2_degs = True
                break
    return is_deg_belongs_2_degs


# Retrieve previously reported data from DHIS2 so that the user can edit it.
def get_data_from_dhis2(passcode, dataset, orgunit, period):

    try:
        user = DHIS2User.objects.get(passcode=passcode)
        api = Api(user.instance.url, user.instance.username,
                  user.instance.password)

        logger.info('Getting data for dataset = {} orgunit = {} period = {}'.format(
            dataset, orgunit, period))
        response = api.get('dataValueSets', params={
            'dataSet': dataset,
            'orgUnit': orgunit,
            'period': period
        })

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(response.json())

    except DHIS2User.DoesNotExist:
        logger.error(
            "DHIS2 user with passcode {} doesn't exist.".format(passcode))
    except RequestException as ex:
        logger.error(ex)
    return {}


def store_data_value_set(data_set, org_unit, passcode, period, phone_number):
    try:
        ds = Dataset.objects.get(dataset_id=data_set)
        ou = OrgUnit.objects.get(org_unit_id=org_unit)
        user = DHIS2User.objects.get(passcode=passcode)
    except Dataset.DoesNotExist:
        logger.error("Dataset with ID {} doesn't exist.".format(data_set))
        return None
    except OrgUnit.DoesNotExist:
        logger.error("Org unit with ID {} doesn't exist.".format(org_unit))
        return None
    except DHIS2User.DoesNotExist:
        logger.error(
            "DHIS2 user with passcode {} doesn't exist.".format(passcode))
        return None
    else:
        data_value_set = DataValueSet.objects.get_or_none(
            data_set=ds, org_unit=ou, user=user, period=period)
        if data_value_set is None:
            data_value_set = DataValueSet()

        data_value_set.data_set = ds
        data_value_set.org_unit = ou
        data_value_set.user = user
        data_value_set.period = period
        data_value_set.phone_number = phone_number
        data_value_set.status = "Pending"
        data_value_set.save()

    return data_value_set


def store_data_value(data_value_set, data_element, category_option_combo, value, session_id):
    try:
        de = DataElement.objects.get(data_element_id=data_element)
        coc = CategoryOptionCombo.objects.get(
            category_option_combo_id=category_option_combo)
    except DataElement.DoesNotExist:
        logger.error(
            "DataElement with ID {} doesn't exist.".format(data_element))
    except CategoryOptionCombo.DoesNotExist:
        logger.error("Category option combo with ID {} doesn't exist.".format(
            category_option_combo))
    else:
        data_value = DataValue.objects.get_or_none(
            data_element=de, category_option_combo=coc, data_value_set=data_value_set)
        if data_value is None:
            data_value = DataValue()

        data_value.data_element = de
        data_value.category_option_combo = coc
        data_value.data_value_set = data_value_set
        data_value.value = value
        data_value.session_id = session_id
        data_value.save()
