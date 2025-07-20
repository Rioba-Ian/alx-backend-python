from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from .models import CustomUser, Conversation, Message
from .serializers import CustomUserSerializer, ConversationSerializer, MessageSerializer

# Create your views here.


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "participants__first_name",
        "participants__last_name",
        "participants_id__email",
    ]

    def get_queryset(self):
        user = self.request.user
        return user.conversations.all().prefetch_related(
            "participants_id", "message_set"
        )

    def perform_create(self, serializer):
        serializer.save(participants_id=[self.request.user]).save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        return Message.objects.filter(
            sender_id=self.request.user, conversation__conversation_id=conversation_id
        ).select_related("sender_id")

    def perform_create(self, serializer):
        serializer.save(sender_id=self.request.user)
