from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404


from .permissions import IsOwnerOrParticipant

# Create your views here.


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrParticipant]
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

    def create(self, request, *args, **kwargs):
        """
        Create new conversation with the authenticated user as a participant.

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participants_data = request.data.get("participants", [])
        participants_ids = [p["id"] for p in participants_data if "id" in p]

        if not participants_ids:
            return Response(
                {"detail": "At least one participant is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create(
            owner=request.user, participants_id=[request.user.id] + participants_ids
        )
        conversation.participants.add(*participants_ids)
        conversation.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(participants_id=[self.request.user]).save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrParticipant]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        return Message.objects.filter(
            sender_id=self.request.user, conversation__conversation_id=conversation_id
        ).select_related("sender_id")

    def create(self, request, *args, **kwargs):
        """
        Send a message in a conversation.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = serializer.validated_data.get("conversation")
        conversation = get_object_or_404(
            Conversation,
            conversation_id=conversation.conversation_id,
        )

        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender_id=request.user,
            content=serializer.validated_data.get("content"),
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(sender_id=self.request.user)
