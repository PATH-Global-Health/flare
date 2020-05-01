import africastalking
import logging
from asgiref. sync import async_to_sync 
from celery import shared_task
from channels. layers import get_channel_layer
from time import sleep
from django.conf import settings
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

    africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)

    # Initialize the SMS service
    sms = africastalking.SMS

    to = ["+251911607571"]
    try:
        response = sms.send(message.content, to)
        logger.info(response)
        
        message.status = "sent"
        message.save()
    except Exception as e:
        message.status = "error"
        message.save()
        logger.info('Encountered an error while sending: %s' % str(e))

    
    channel_layer = get_channel_layer()
    logger.info("Sending message")
    async_to_sync(channel_layer.group_send)(
        'message' , { 'type' : 'message.sent','content' : {'state':'complete', 'messageId':message.id} }
    )