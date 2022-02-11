import logging
from datetime import datetime

from .models import OrgUnit

logger = logging.getLogger(__name__)


def sync_org_units(api, dhis2_instance):
    logger.info("Starting to sync org units")

    for pages in api.get_paged('organisationUnits', page_size=100, params={'fields': 'id,displayName,parent'}):
        for org_unit in pages['organisationUnits']:
            ou = OrgUnit.objects.get_or_none(ou_id=org_unit['id'])

            if ou is None:
                ou = OrgUnit()

            ou.ou_id = org_unit['id']
            ou.name = org_unit['displayName'] if 'displayName' in org_unit else "No Name"
            ou.parent = org_unit['parent']['id'] if 'parent' in org_unit else ''
            ou.instance = dhis2_instance

            ou.save()

    logger.info("Syncing org units  ............ Done")
