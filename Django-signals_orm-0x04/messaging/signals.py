from .models import Message, Notification

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user_id=instance.receiver,
            message_id=instance,
            content=f"""New message from
            {instance.sender.username}:
            {instance.content}""",
        )
