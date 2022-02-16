import json
import logging
import redis
from datetime import datetime
from typing import List

from django.conf import settings

from .models import OrgUnit, DHIS2User, Dataset, CategoryCombo, CategoryOptionCombo, \
    DataElement, Section, SectionDataElement, UserGroup
from .utils import unique_passcode

logger = logging.getLogger(__name__)
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0, decode_responses=True)


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

    user_groups = UserGroup.objects.filter(instance=dhis2_instance)

    for user_group in user_groups:
        for pages in api.get_paged('users', page_size=100,
                                   params={'fields': 'id,displayName,userCredentials,organisationUnits',
                                           'filter': 'userGroups.id:eq:{}'.format(user_group.group_id)}):
            for user in pages['users']:
                usr = DHIS2User.objects.get_or_none(user_id=user['id'])

                if usr is None:
                    usr = DHIS2User()
                usr.user_id = user['id']
                usr.name = user['displayName'] if 'displayName' in user else "No Name"
                usr.username = user['userCredentials']['username'] if 'userCredentials' in user else ""
                if usr.passcode is None:
                    usr.passcode = unique_passcode()
                usr.group = user_group
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


def sync_category_combos(api, dhis2_instance, version):
    logger.info("Starting to sync category combos")

    for pages in api.get_paged('categoryCombos', page_size=100,
                               params={'fields': 'id,name,categoryOptionCombos[id,name]'}):
        for cat_combo in pages['categoryCombos']:
            cc = CategoryCombo.objects.get_or_none(category_combo_id=cat_combo['id'])

            if cc is None:
                cc = CategoryCombo()

            cc.category_combo_id = cat_combo['id']
            cc.name = cat_combo['name'] if 'name' in cat_combo else "No Name"
            cc.version = version
            cc.instance = dhis2_instance
            cc.save()

            if 'categoryOptionCombos' in cat_combo:
                for coc in cat_combo['categoryOptionCombos']:
                    coc_obj = CategoryOptionCombo.objects.get_or_none(category_option_combo_id=coc['id'])
                    if coc_obj is None:
                        coc_obj = CategoryOptionCombo()

                    coc_obj.category_option_combo_id = coc['id']
                    coc_obj.name = coc['name']
                    coc_obj.category_combo = cc
                    coc_obj.version = version
                    coc_obj.instance = dhis2_instance
                    coc_obj.save()

    CategoryCombo.objects.exclude(version=version, instance=dhis2_instance).delete()
    CategoryOptionCombo.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing category combos ............ Done")


def sync_data_elements(api, dhis2_instance, version):
    logger.info("Starting to sync data elements")

    for pages in api.get_paged('dataElements', page_size=100, params={'fields': 'id,formName,categoryCombo,valueType'}):
        for data_element in pages['dataElements']:
            de = DataElement.objects.get_or_none(data_element_id=data_element['id'])

            if de is None:
                de = DataElement()
            de.data_element_id = data_element['id']
            de.name = data_element['formName'] if 'formName' in data_element else "No Name"
            de.value_type = data_element['valueType'] if 'valueType' in data_element else "No Name"
            de.category_combo = CategoryCombo.objects.get_or_none(category_combo_id=data_element['categoryCombo']['id'])
            de.version = version
            de.instance = dhis2_instance

            de.save()

    DataElement.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing data elements ............ Done")


def sync_data_sets(api, dhis2_instance, version):
    logger.info("Starting to sync data sets")

    for pages in api.get_paged('dataSets', page_size=100,
                               params={'fields': 'id,displayName,dataSetElements,organisationUnits'}):
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

            # save the org units assigned to the dataset
            if 'organisationUnits' in dataset:
                for org_unit in dataset['organisationUnits']:
                    ou = OrgUnit.objects.get_or_none(org_unit_id=org_unit['id'])
                    if ou is not None:
                        ds.org_units.add(ou)
                ds.save()

            ds.data_element.clear()
            # save the data elements that the dataset contains
            if 'dataSetElements' in dataset:
                for data_element in dataset['dataSetElements']:
                    de = DataElement.objects.get_or_none(data_element_id=data_element['dataElement']['id'])
                    if de is not None:
                        ds.data_element.add(de)
                ds.save()

    Dataset.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing data sets ............ Done")


def sync_sections(api, dhis2_instance, version):
    logger.info("Starting to sync sections")

    for pages in api.get_paged('sections', page_size=100,
                               params={'fields': 'id,displayName,dataSet,sortOrder,dataElements'}):
        for section in pages['sections']:
            sec = Section.objects.get_or_none(section_id=section['id'])

            if sec is None:
                sec = Section()
            sec.section_id = section['id']
            sec.name = section['displayName'] if 'displayName' in section else "No Name"
            sec.version = version
            sec.instance = dhis2_instance
            sec.sort_order = section['sortOrder']
            sec.dataset = Dataset.objects.get_or_none(dataset_id=section['dataSet']['id'])

            sec.save()

            # save the data elements that the section contains
            if 'dataElements' in section:
                sort_order = 0
                for data_element in section['dataElements']:
                    de = DataElement.objects.get_or_none(data_element_id=data_element['id'])
                    if de is not None:
                        sec_de = SectionDataElement()
                        sec_de.data_element = de
                        sec_de.section = sec
                        sort_order += 1
                        sec_de.sort_order = sort_order
                        sec_de.version = version
                        sec_de.save()

                SectionDataElement.objects.exclude(version=version).delete()

    Section.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing sections ............ Done")


def invalidate_users_cache():
    for user in DHIS2User.objects.all():
        redis_instance.unlink(user.passcode)
    logger.info("Invalidating users from cache ............ Done")


def invalidate_org_units_cache():
    for user in DHIS2User.objects.all():
        for ou in user.org_units.all():
            redis_instance.unlink("ou_{}".format(ou.org_unit_id))
    logger.info("Invalidating org units from cache ............ Done")


def invalidate_dataset_cache():
    for dataset in Dataset.objects.all():
        redis_instance.unlink("ds_{}".format(dataset.dataset_id))
    logger.info("Invalidating datasets from cache ............ Done")


# passcode1: {
#               1: {name: org_unit_name1, id: org_unit_id1},
#               2: {name: org_unit_name2, id: org_unit_id2}
#            }
# passcode2: {
#               1: {name: org_unit_name1, id: org_unit_id1},
#               2: {name: org_unit_name2, id: org_unit_id2}
#               3: {name: org_unit_name3, id: org_unit_id3}
#            }

def cache_users_with_their_assigned_org_units() -> List[dict]:
    org_units_to_cache = []
    users = DHIS2User.objects.all()
    for user in users:
        user_ou = {}
        for i, ou in enumerate(user.org_units.all()):
            user_ou[i + 1] = {'name': ou.name, 'id': ou.org_unit_id}

            if ou.org_unit_id not in org_units_to_cache:
                org_units_to_cache.append(ou.org_unit_id)

        redis_instance.set(user.passcode, json.dumps(user_ou))

    logger.info('Caching user with their assigned org units ............ Done')

    return org_units_to_cache


# orgunit_id_1: {
#               1: {name: dataset_name1, id: dataset_id1},
#               2: {name: dataset_name2, id: dataset_id2}
#            }
# orgunit_id_2: {
#               1: {name: dataset_name1, id: dataset_id1},
#               2: {name: dataset_name2, id: dataset_id2}
#               3: {name: dataset_name3, id: dataset_id3}
#            }
def cache_org_units_with_their_datasets(org_units_to_cache):
    for ou in org_units_to_cache:
        org_unit = OrgUnit.objects.get_or_none(org_unit_id=ou)
        if org_unit is not None:
            datasets = org_unit.dataset_set.all()
            org_unit_datasets = {}
            for i, dataset in enumerate(datasets):
                org_unit_datasets[i + 1] = {'name': dataset.name, 'id': dataset.dataset_id}

            redis_instance.set("ou_{}".format(org_unit.org_unit_id), json.dumps(org_unit_datasets))

    logger.info('Caching org units with their datasets ............ Done')


# dataset_id_1: {
#               1: {
#                       name: section_name1,
#                       id: section_id1
#                       dataelements: [
#                           {
#                               dataelement_name: dataelement_name1,
#                               dataelement_id: dataelement_id1,
#                               catoptioncombo_name: catoptioncombo_name1,
#                               categoryoptioncombo_id: categoryoptioncombo_id,
#                               dataelement_value_type: dataelement_value_type
#                           }
#                       ]
#                  },
#               2: {
#                       name: section_name2,
#                       id: section_id2
#                       dataelements: [
#                           {
#                                dataelement_name: dataelement_name2,
#                                dataelement_id: dataelement_id2,
#                                catoptioncombo_name: catoptioncombo_name2,
#                                categoryoptioncombo_id: categoryoptioncombo_id2,
#                                dataelement_value_type: dataelement_value_type
#                            }
#                        ]
#               }
#            }

def cache_datasets_with_their_data_elements():
    for dataset in Dataset.objects.all():
        dataset_sections = {}
        for i, section in enumerate(dataset.section_set.all()):
            dataset_sections[i + 1] = {'name': section.name, 'id': section.section_id, 'dataelements': []}
            for sec_de in section.sectiondataelement_set.all():
                de = sec_de.data_element
                for coc in de.category_combo.categoryoptioncombo_set.all():
                    dataset_sections[i + 1]['dataelements'].append(
                        {
                            'dataelement_name': de.name,
                            'dataelement_id': de.data_element_id,
                            'catoptioncombo_name': coc.name,
                            'categoryoptioncombo_id': coc.category_option_combo_id,
                            'dataelement_value_type': de.value_type
                        }
                    )

        redis_instance.set("ds_{}".format(dataset.dataset_id), json.dumps(dataset_sections))

    logger.info('Caching datasets with sections, dataelements and category combos  ............ Done')
