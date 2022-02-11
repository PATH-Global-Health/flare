import uuid
import logging
from celery import shared_task
from dhis2 import Api

from .models import DHIS2Instance, OrgUnit
from .helper import sync_org_units, sync_users

logger = logging.getLogger(__name__)


@shared_task
def sync_dhis2_metadata():
    logger.info("Starting to sync metadata")

    dhis2_instances = DHIS2Instance.objects.all()
    for dhis2 in dhis2_instances:
        api = Api(dhis2.url, dhis2.username, dhis2.password)
        version = uuid.uuid4()

        logger.info("Downloading metadata from {} with version {}.".format(dhis2.url, version))

        sync_org_units(api, dhis2, version)
        sync_users(api, dhis2, version)

    logger.info("Syncing metadata ............ Done")
