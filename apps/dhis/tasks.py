import uuid
import logging
from celery import shared_task
from dhis2 import Api

from .models import Instance, OrgUnit
from .helper import sync_org_units, sync_users, sync_data_sets, sync_category_combos, sync_data_elements,\
    sync_sections, invalidate_users_cache, invalidate_org_units_cache, invalidate_dataset_cache,\
    cache_users_with_their_assigned_org_units,cache_org_units_with_their_datasets,\
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
