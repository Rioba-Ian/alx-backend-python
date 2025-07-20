from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_id = CustomUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender_id", "message_body", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    participants_id = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants_id", "created_at", "updated_at"]
