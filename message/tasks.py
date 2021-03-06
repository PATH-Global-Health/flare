from asgiref. sync import async_to_sync 
from celery import shared_task
from channels. layers import get_channel_layer
from time import sleep
from .models import Message
from .helpers import send_sms_using_africas_talking, send_message_to_telegram
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_message(message_id):
    
    message = Message.objects.get(pk=message_id)

    status = True
    for channel in message.channels.all():
        if channel.id == 1:
            status = status & send_sms_using_africas_talking(message)
        if channel.id == 2:
            status = status & send_message_to_telegram(message)

    status_str = 'sent' if status else 'error'

    message.status = status_str
    message.save()

    channel_layer = get_channel_layer()
    
    async_to_sync(channel_layer.group_send)(
        'message' , { 'type' : 'message.sent','content' : 
        {'action':'CHANGE_MESSAGE_STATUS','status': status_str , 'messageId':message.id} }
    )