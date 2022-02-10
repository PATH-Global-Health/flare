from celery import shared_task
from time import sleep
from .models import DHIS2Instance, OrgUnit


@shared_task
def sync_metadata():
    pass
    # org_unit = OrgUnit.objects.get(pk=message_id)

