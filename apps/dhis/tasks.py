import uuid
import logging
from celery import shared_task
from dhis2 import Api

from .models import Instance, OrgUnit, Dataset, DataElement, CategoryOptionCombo, DHIS2User, DataValueSet, DataValue
from apps.dhis.ussd.helper import sync_org_units, sync_users, sync_data_sets, sync_category_combos, \
    sync_data_elements, sync_sections, invalidate_users_cache, invalidate_org_units_cache, invalidate_dataset_cache, \
    cache_users_with_their_assigned_org_units, cache_org_units_with_their_datasets, \
    cache_datasets_with_their_data_elements

logger = logging.getLogger(__name__)


@shared_task
def sync_dhis2_metadata():
    invalidate_users_cache()
    invalidate_org_units_cache()
    invalidate_dataset_cache()

    logger.info("Starting to sync metadata")

    dhis2_instances = Instance.objects.all()
    for dhis2 in dhis2_instances:
        api = Api(dhis2.url, dhis2.username, dhis2.password)
        version = uuid.uuid4()

        logger.info("Downloading metadata from {} with version {}.".format(dhis2.url, version))

        sync_org_units(api, dhis2, version)
        sync_users(api, dhis2, version)
        sync_category_combos(api, dhis2, version)
        sync_data_elements(api, dhis2, version)
        sync_data_sets(api, dhis2, version)
        sync_sections(api, dhis2, version)

    logger.info("Syncing metadata ............ Done")

    org_units_to_cache = cache_users_with_their_assigned_org_units()
    cache_org_units_with_their_datasets(org_units_to_cache)
    cache_datasets_with_their_data_elements()


@shared_task
def cache_dhis2_metadata():
    invalidate_users_cache()
    invalidate_org_units_cache()
    invalidate_dataset_cache()

    org_units_to_cache = cache_users_with_their_assigned_org_units()
    cache_org_units_with_their_datasets(org_units_to_cache)
    cache_datasets_with_their_data_elements()


@shared_task
def save_to_database(data_set, data_element, category_option_combo, org_unit, passcode, period, value, phone_number):
    try:
        ds = Dataset.objects.get(dataset_id=data_set)
        de = DataElement.objects.get(data_element_id=data_element)
        coc = CategoryOptionCombo.objects.get(category_option_combo_id=category_option_combo)
        ou = OrgUnit.objects.get(org_unit_id=org_unit)
        user = DHIS2User.objects.get(passcode=passcode)

    except Dataset.DoesNotExist:
        logger.error("Dataset with ID {} doesn't exist.".format(data_set))
    except DataElement.DoesNotExist:
        logger.error("DataElement with ID {} doesn't exist.".format(data_element))
    except CategoryOptionCombo.DoesNotExist:
        logger.error("Category option combo with ID {} doesn't exist.".format(category_option_combo))
    except OrgUnit.DoesNotExist:
        logger.error("Org unit with ID {} doesn't exist.".format(org_unit))
    except DHIS2User.DoesNotExist:
        logger.error("DHIS2 user with passcode {} doesn't exist.".format(passcode))
    else:
        data_value_set = DataValueSet.objects.get_or_none(data_set=ds, org_unit=ou, user=user, period=period)
        if data_value_set is None:
            data_value_set = DataValueSet()

        data_value_set.data_set = ds
        data_value_set.org_unit = ou
        data_value_set.user = user
        data_value_set.period = period
        data_value_set.phone_number = phone_number
        data_value_set.status = "Pending"
        data_value_set.save()

        data_value = DataValue.objects.get_or_none(
            data_element=de, category_option_combo=coc, data_value_set=data_value_set)
        if data_value is None:
            data_value = DataValue()

        data_value.data_element = de
        data_value.category_option_combo = coc
        data_value.data_value_set = data_value_set
        data_value.value = value
        data_value.save()
        logger.info("Saved data into database \n\tData set: {}\n\tData element: {}\n\tCategory option combo: {}\n\tOrg unit: {}\n\tPasscode: {}\n\tPeriod: {}\n\tPhone number: {}\n\tValue: {}"
                    .format(ds.name, de.name, coc.name, ou.name, passcode, period, phone_number, value))
