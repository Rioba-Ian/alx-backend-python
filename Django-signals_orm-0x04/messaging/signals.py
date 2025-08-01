from .models import Message, Notification, MessageHistory, CustomUser

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


@receiver(post_save, sender=CustomUser)
def cleanup_user_after_delete(sender, instance, **kwargs):
    """
    Clean up user-related data after a user is deleted.
    """
    # Delete all messages sent by the user
    Message.objects.filter(sender=instance).delete()

    # Delete all messages received by the user
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications related to the user
    Notification.objects.filter(user_id=instance).delete()

    # Delete all conversations the user was part of
    MessageHistory.objects.filter(edited_by=instance.id).delete()
