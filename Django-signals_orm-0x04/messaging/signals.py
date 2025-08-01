from .models import Message, Notification, MessageHistory

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


@receiver(post_save, sender=Message)
def post_save_message_history(sender, instance, created, **kwargs):
    if instance.edited:
        try:
            original_message = Message.objects.get(
                message_id=instance.message_id,
            )
            if original_message.content != instance.content:
                MessageHistory.objects.create(
                    message=original_message,
                    previous_content=original_message.content,
                    edited_by=instance.sender,
                )
                instance.edited = True
                instance.save()
        except Message.DoesNotExist:
            # Handle the case where the original message does not exist
            pass
