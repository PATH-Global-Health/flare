from celery import shared_task
from time import sleep
from .models import DHIS2Instance, OrgUnit
from .helper import sync_org_units, sync_users
from dhis2 import Api


@shared_task
def sync_dhis2_metadata():

    dhis2_instances = DHIS2Instance.objects.all()
    for dhis2 in dhis2_instances:
        api = Api(dhis2.url, dhis2.username, dhis2.password)
        sync_org_units(api, dhis2)
        sync_users(api, dhis2)
