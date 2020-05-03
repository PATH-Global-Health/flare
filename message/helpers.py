import africastalking
import logging
import telegram
from subscriber.models import Subscriber
from settings.models import Configuration
from .models import MessageStatus

logger = logging.getLogger(__name__)

# Africas talking

def send_sms_using_africas_talking(message):
    logger.info("Initializing Africa's Talking")
    status = ''
    sms = None
    try:
        config = Configuration.objects.get(pk=1)
        africastalking.initialize(config.user_id, config.token)
        
        # Initialize the SMS service
        sms = africastalking.SMS
    except Configuration.DoesNotExist:
        logger.error("Africa's Talking configration doesn't exist")
        update_message_status(None, message.id, 0, 0, True)
        return False

    status = send_sms_2_african_talking_endpoint(config, message, sms)

    return status == 'sent'

def send_sms_2_african_talking_endpoint(config, message, sms):
    success_count = 0
    error_count = 0

    for lang in message.languages.all():
        subscriber_set = Subscriber.objects.filter(language_id=lang.id)

        for subscriber in subscriber_set:
            try:
                response = sms.send(message.content, [subscriber.phone_number])
                logger.info(response)
                success_count += 1
            except Exception as e:
                logger.info('Encountered an error while sending: %s' % str(e))
                error_count += 1

    update_message_status(config.id, message.id, success_count, error_count)

    status = 'error'
    if(success_count >= error_count):
        status = 'sent'

    return status

# telegram 

def send_message_to_telegram(message):
    status = False

    for lang in message.languages.all():
        try:
            config = Configuration.objects.get(language_id=lang.id)
            status = status | send_message_to_bot(config, message)
        except Configuration.DoesNotExist:
            logger.error("Telegram configration doesn't exist")
            update_message_status(None, message.id, 0, 0, True)
            return False
    return status

def send_message_to_bot(config, message):
    try:
        bot = telegram.Bot(token=config.token)
        bot.sendMessage(chat_id=config.user_id, text=message.content)
        update_message_status(config.id, message.id, 1, 0)
        logger.info("Message with message_id {} and channel_id {} is sent successfully.".format(message.id, config.id))
        return True
    except Exception:
        update_message_status(config.id, message.id, 0, 1)
        logger.error("Sending message with message_id {} and channel_id {} failed.".format(message.id, config.id))
        return False

# Common 

def update_message_status(config_id, message_id, success_count, error_count, config_error=False):
    msg_status = MessageStatus()
    msg_status.message_id = message_id
    msg_status.configuration_id = config_id
    msg_status.success_count = success_count
    msg_status.error_count = error_count
    msg_status.config_error = config_error
    msg_status.save()

