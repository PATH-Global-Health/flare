import logging
from asgiref. sync import async_to_sync 
from celery import shared_task
from channels. layers import get_channel_layer
from time import sleep
from .models import Message

@shared_task
def send_message(message_id):
    
    logger = logging.getLogger()
    logger.info("=====================================================================")
    message = Message.objects.get(pk=message_id)
    # languages = message.languages.all()
    for lang in message.languages.all():
        print(lang.name)
    logger.info("=====================================================================")
    # sleep(10)
    message.status = "sent"
    message.save()
    channel_layer = get_channel_layer()
    logger.info("Sending message")
    async_to_sync(channel_layer.group_send)(
        'message' , { 'type' : 'message.sent','content' : {'state':'complete', 'messageId':message.id} }
    )