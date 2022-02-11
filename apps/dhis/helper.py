import logging
from datetime import datetime

from .models import OrgUnit, DHIS2User

logger = logging.getLogger(__name__)


def sync_org_units(api, dhis2_instance, version):
    logger.info("Starting to sync org units")

    for pages in api.get_paged('organisationUnits', page_size=100, params={'fields': 'id,displayName,parent'}):
        for org_unit in pages['organisationUnits']:
            ou = OrgUnit.objects.get_or_none(ou_id=org_unit['id'])

            if ou is None:
                ou = OrgUnit()

            ou.ou_id = org_unit['id']
            ou.name = org_unit['displayName'] if 'displayName' in org_unit else "No Name"
            ou.parent = org_unit['parent']['id'] if 'parent' in org_unit else ''
            ou.version = version
            ou.instance = dhis2_instance

            ou.save()

    OrgUnit.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing org units ............ Done")


def sync_users(api, dhis2_instance, version):
    logger.info("Starting to sync users")

    for pages in api.get_paged('users', page_size=100, params={'fields': 'id,displayName,userCredentials,organisationUnits'}):
        for user in pages['users']:
            usr = DHIS2User.objects.get_or_none(user_id=user['id'])

            if usr is None:
                usr = DHIS2User()
            usr.user_id = user['id']
            usr.name = user['displayName'] if 'displayName' in user else "No Name"
            usr.username = user['userCredentials']['username'] if 'userCredentials' in user else ""
            usr.version = version
            usr.instance = dhis2_instance

            usr.save()

            if 'organisationUnits' in user:
                for org_unit in user['organisationUnits']:
                    ou = OrgUnit.objects.get_or_none(ou_id=org_unit['id'])
                    if ou is not None:
                        usr.orgUnits.add(ou)
                    usr.save()

    DHIS2User.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing users ............ Done")
