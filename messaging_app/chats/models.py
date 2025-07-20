from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=50,
        choices=[("admin", "Admin"), ("guest", "Guest", "host", "Host")],
        default="guest",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    message_body = models.TextField(not_null=True)
    sent_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    participants_id = models.ManyToManyField(CustomUser, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
