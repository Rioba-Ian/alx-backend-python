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
    sender_username = serializers.CharField(source="sender_id.username", read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender_id",
            "message_body",
            "sent_at",
            "sender_username",
        ]

    def create(self, validated_data):
        sender = validated_data.pop("sender_id")
        message = Message.objects.create(sender_id=sender, **validated_data)
        return message


class ConversationSerializer(serializers.ModelSerializer):
    participants_id = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source="message_set")
    participant_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants_id",
            "participant_count",
            "messages",
            "last_message",
            "uncread_count," "created_at",
            "updated_at",
        ]

    def get_participant_count(self, obj):
        return obj.participants_id.count()

    def get_last_message(self, obj):
        last_message = obj.message_set.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_unread_count(self, obj):
        """
        Assuming we have a way to track unread messages,
        this is a placeholder
        """
        return (
            obj.message_set.filter(read=False).count()
            if hasattr(obj, "message_set")
            else 0
        )

    def validate(self, data):
        if "participants_id" not in data or not data["participants_id"]:
            raise serializers.ValidationError("At least one participant is required.")
        return data

    def create(self, validated_data):
        participants = validated_data.pop("participants_id", [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants_id.set(participants)
        return conversation
