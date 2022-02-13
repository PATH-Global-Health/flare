import logging
from datetime import datetime

from .models import OrgUnit, DHIS2User, Dataset, CategoryCombo

logger = logging.getLogger(__name__)


def sync_org_units(api, dhis2_instance, version):
    logger.info("Starting to sync org units")

    for pages in api.get_paged('organisationUnits', page_size=100, params={'fields': 'id,displayName,parent'}):
        for org_unit in pages['organisationUnits']:
            ou = OrgUnit.objects.get_or_none(org_unit_id=org_unit['id'])

            if ou is None:
                ou = OrgUnit()

            ou.org_unit_id = org_unit['id']
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
            usr.org_units.clear()

            if 'organisationUnits' in user:
                for org_unit in user['organisationUnits']:
                    ou = OrgUnit.objects.get_or_none(org_unit_id=org_unit['id'])
                    if ou is not None:
                        usr.org_units.add(ou)
                usr.save()

    DHIS2User.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing users ............ Done")


def sync_data_sets(api, dhis2_instance, version):
    logger.info("Starting to sync data sets")

    for pages in api.get_paged('dataSets', page_size=100, params={'fields': 'id,displayName,dataSetElements,organisationUnits'}):
        for dataset in pages['dataSets']:
            ds = Dataset.objects.get_or_none(dataset_id=dataset['id'])

            if ds is None:
                ds = Dataset()
            ds.dataset_id = dataset['id']
            ds.name = dataset['displayName'] if 'displayName' in dataset else "No Name"
            ds.version = version
            ds.instance = dhis2_instance

            ds.save()
            ds.org_units.clear()

            if 'organisationUnits' in dataset:
                for org_unit in dataset['organisationUnits']:
                    ou = OrgUnit.objects.get_or_none(org_unit_id=org_unit['id'])
                    if ou is not None:
                        ds.org_units.add(ou)
                ds.save()

    Dataset.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing data sets ............ Done")


def sync_category_combos(api, dhis2_instance, version):
    logger.info("Starting to sync category combos")

    for pages in api.get_paged('categoryCombos', page_size=100, params={'fields': 'id,name,categoryOptionCombos[id,name]'}):
        for cat_combo in pages['categoryCombos']:
            cc = CategoryCombo.objects.get_or_none(category_combo_id=cat_combo['id'])

            if cc is None:
                cc = CategoryCombo()

            cc.category_combo_id = cat_combo['id']
            cc.name = cat_combo['name'] if 'name' in cat_combo else "No Name"
            cc.version = version
            cc.instance = dhis2_instance

            cc.save()

    CategoryCombo.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing category combos ............ Done")
