from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Message
from .tasks import send_message


@receiver(m2m_changed, sender=Message.languages.through)
@receiver(m2m_changed, sender=Message.channels.through)
def announce_new_message(sender, **kwargs):
    if kwargs.get('action') == "post_add":
        msg = kwargs['instance']
        if msg.languages.all().count() > 0 and msg.channels.all().count() > 0:
            # Start long running task here (using Celery)
            send_message_task = send_message.delay(msg.id)

            # Store the celery task id into the database if we wanted to
            # do things like cancel the task in the future
            msg.celery_id = send_message_task.id
            msg.save()
