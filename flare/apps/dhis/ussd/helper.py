import logging
from datetime import datetime
from typing import List

from django.conf import settings

from apps.dhis.models import OrgUnit, DHIS2User, Dataset, CategoryCombo, CategoryOptionCombo, \
    DataElement, Section, UserGroup, DatasetDataElement
from apps.dhis.utils import unique_passcode, store_data_elements_assigned_2_dataset, \
    store_org_units_assigned_2_dataset, format_dataset_with_section, format_dataset_with_out_section
from apps.dhis.ussd.store import Store

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
                for index, coc in enumerate(cat_combo['categoryOptionCombos']):
                    coc_obj = CategoryOptionCombo.objects.get_or_none(category_option_combo_id=coc['id'])
                    if coc_obj is None:
                        coc_obj = CategoryOptionCombo()

                    coc_obj.category_option_combo_id = coc['id']
                    coc_obj.name = coc['name']
                    coc_obj.sort_order = index + 1
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
    logger.info("Starting to sync dataset")

    for pages in api.get_paged('dataSets', page_size=100,
                               params={'fields': 'id,name,shortName,periodType,dataSetElements,organisationUnits,openFuturePeriods,compulsoryDataElementOperands'}):
        for dataset in pages['dataSets']:
            ds = Dataset.objects.get_or_none(dataset_id=dataset['id'])

            if ds is None:
                ds = Dataset()
            ds.dataset_id = dataset['id']
            ds.name = dataset['shortName'] if 'shortName' in dataset else dataset['name']
            ds.period_type = dataset['periodType'] if 'periodType' in dataset else ""

            try:
                ds.open_future_periods = int(dataset['openFuturePeriods']) if 'openFuturePeriods' in dataset else 0
            except ValueError:
                ds.open_future_periods = 0

            ds.version = version
            ds.instance = dhis2_instance

            ds.save()
            ds.org_units.clear()

            # save the org units assigned to the dataset
            if 'organisationUnits' in dataset:
                store_org_units_assigned_2_dataset(ds, dataset['organisationUnits'])

            ds.data_element.clear()
            # save the data elements that the dataset contains in DatasetDataElement table
            if 'dataSetElements' in dataset:
                store_data_elements_assigned_2_dataset(ds, dataset, version, dhis2_instance)

    Dataset.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing dataset ............ Done")


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
                        for coc in de.category_combo.categoryoptioncombo_set.all().order_by('sort_order'):
                            ds_de = DatasetDataElement.objects.get_or_none(data_set__dataset_id=section['dataSet']['id'],
                                                                           data_element__data_element_id=de.data_element_id,
                                                                           category_option_combo__category_option_combo_id=coc.category_option_combo_id)
                            if ds_de is not None:
                                sort_order += 1
                                ds_de.sort_order = sort_order
                                ds_de.section = sec
                                ds_de.save()

    Section.objects.exclude(version=version, instance=dhis2_instance).delete()

    logger.info("Syncing sections ............ Done")


def invalidate_users_cache():
    for user in DHIS2User.objects.all():
        Store.unlink("usr_{}".format(user.passcode))
    logger.info("Invalidating users from cache ............ Done")


def invalidate_org_units_cache():
    for user in DHIS2User.objects.all():
        for ou in user.org_units.all():
            Store.unlink("ou_{}".format(ou.org_unit_id))
    logger.info("Invalidating org units from cache ............ Done")


def invalidate_dataset_cache():
    for dataset in Dataset.objects.all():
        Store.unlink("ds_{}".format(dataset.dataset_id))
    logger.info("Invalidating datasets from cache ............ Done")


# usr_passcode1: {
#               1: {name: org_unit_name1, id: org_unit_id1},
#               2: {name: org_unit_name2, id: org_unit_id2}
#            }
# usr_passcode2: {
#               1: {name: org_unit_name1, id: org_unit_id1},
#               2: {name: org_unit_name2, id: org_unit_id2}
#               3: {name: org_unit_name3, id: org_unit_id3}
#            }

def cache_users_with_assigned_org_units() -> List[dict]:
    org_units_to_cache = []

    for user in DHIS2User.objects.all():
        user_ou = {}
        for i, ou in enumerate(user.org_units.all()):
            user_ou[i + 1] = {'name': ou.name, 'id': ou.org_unit_id}
            if ou.org_unit_id not in org_units_to_cache:
                org_units_to_cache.append(ou.org_unit_id)

        Store.set("usr_{}".format(user.passcode), user_ou)

    logger.info('Caching users ............ Done')

    return org_units_to_cache


# ou_orgunit_id_1: {
#                   1: {
#                           name: dataset_name1,
#                           id: dataset_id1,
#                           period_type: period_type1,
#                           open_future_periods: open_future_periods1
#                           has_section: True,
#                      },
#                   2: {
#                           name: dataset_name2,
#                           id: dataset_id2,
#                           period_type: period_type2,
#                           open_future_periods: open_future_periods2,
#                           has_section: False,
#                      }
#            }
# ou_orgunit_id_2: {
#               ...
#            }
def cache_org_units_with_datasets(org_units_to_cache: List[dict]):
    for ou in org_units_to_cache:
        org_unit = OrgUnit.objects.get_or_none(org_unit_id=ou)
        if org_unit is not None:
            datasets = org_unit.dataset_set.all()
            org_unit_datasets = {}
            for i, dataset in enumerate(datasets):
                # check dataset has section or not
                section_count = dataset.section_set.count()
                has_section = section_count > 0

                org_unit_datasets[i + 1] = {
                    'name': dataset.name,
                    'id': dataset.dataset_id,
                    'period_type': dataset.period_type,
                    'open_future_periods': dataset.open_future_periods,
                    'has_section': has_section
                }

            Store.set("ou_{}".format(org_unit.org_unit_id), org_unit_datasets)

    logger.info('Caching org units ............ Done')


# Data structure of dataset that has a section
# ds_dataset_id_1: {
#               1: {
#                       name: section_name1,
#                       id: section_id1
#                       data_elements: [
#                           {
#                               data_element_name: data_element_name1,
#                               data_element_id: data_element_id1,
#                               category_option_combo_name: category_option_combo_name1,
#                               category_option_combo_id: category_option_combo_id,
#                               data_element_value_type: data_element_value_type,
#                               compulsory: true
#                           }
#                       ]
#                  },
#               2: {
#                       name: section_name2,
#                       id: section_id2
#                       data_elements: [
#                           {
#                                data_element_name: data_element_name2,
#                                data_element_id: data_element_id2,
#                                category_option_combo_name: category_option_combo_name2,
#                                category_option_combo_id: category_option_combo_id2,
#                                data_element_value_type: data_element_value_type
#                                compulsory: false
#                            }
#                        ]
#               }
#            }

# Data structure of dataset that has no section
# ds_dataset_id_1: {
#               data_elements: [
#                   {
#                       data_element_name: data_element_name1,
#                       data_element_id: data_element_id1,
#                       category_option_combo_name: category_option_combo_name1,
#                       category_option_combo_id: category_option_combo_id1,
#                       data_element_value_type: data_element_value_type
#                       compulsory: false
#                   },
#                   {
#                       data_element_name: data_element_name2,
#                       data_element_id: data_element_id2,
#                       category_option_combo_name: category_option_combo_name2,
#                       category_option_combo_id: category_option_combo_id2,
#                       data_element_value_type: data_element_value_type
#                       compulsory: true
#                   }
#               ]
#            }
def cache_datasets_with_data_elements():
    for dataset in Dataset.objects.all():
        formatted_dataset = {}
        sections = dataset.section_set.all().order_by('sort_order')

        if not sections:
            # dataset with no sections
            formatted_dataset['data_elements'] = format_dataset_with_out_section(dataset)
        else:
            # dataset with sections
            formatted_dataset = format_dataset_with_section(sections)


        Store.set("ds_{}".format(dataset.dataset_id), formatted_dataset)

    logger.info('Caching datasets ............ Done')
