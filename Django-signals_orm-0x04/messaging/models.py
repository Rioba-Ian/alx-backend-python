from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class ROLE_CHOICES(models.TextChoices):
    ADMIN = "admin", "Admin"
    GUEST = "guest", "Guest"
    HOST = "host", "Host"


class CustomUser(AbstractUser):
    user_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=50,
        choices=[
            (ROLE_CHOICES.ADMIN, "Admin"),
            (ROLE_CHOICES.GUEST, "Guest"),
            (ROLE_CHOICES.HOST, "Host"),
        ],
        default="guest",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)


class MessageHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    previous_content = models.TextField(null=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="edited_messages"
    )

    class Meta:
        ordering = ["-edited_at"]

    def __str__(self) -> str:
        return f"History of message {self.message.message_id} edited {self.edited_by.username} at {self.edited_at}"


class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    participants_id = models.ManyToManyField(
        CustomUser,
        related_name="conversations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    message_id = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="notifications"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
