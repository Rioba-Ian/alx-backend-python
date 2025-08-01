from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, Notification, MessageHistory
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    NotificationSerializer,
    MessageHistorySerializer,
)
from django.shortcuts import get_object_or_404
import django_filters
from .filters import MessageFilter
from .pagination import StandardResultsSetPagination
from .permissions import IsOwnerOrParticipant
from rest_framework.views import APIView

from rest_framework.decorators import api_view, permission_classes

# Create your views here.


class ConversationFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Conversation
        fields = ["created_at"]


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
        return (
            Conversation.objects.filter(participants__in=[user])
            .select_related("owner")
            .prefetch_related("participants")
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
    pagination_class = StandardResultsSetPagination
    filter_backends = filters.DjangoFilterBackend
    filterset_class = MessageFilter

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

    def thread(self, request, pk=None):
        message = self.get_object()
        threaded = build_threaded_message(message)
        return Response(threaded, status=status.HTTP_200_OK)


class UnreadMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        unread_messages = Message.unread.unread_for_user(user)
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user_id=user).select_related(
            "message_id",
        )


class MessageHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = MessageHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MessageHistory.objects.filter(edited_by=user).select_related(
            "message", "edited_by"
        )

    def perform_create(self, serializer):
        serializer.save(edited_by=self.request.user)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    """
    Delete the currently authenticated user and all their associated data.
    """
    try:
        user = request.user
        if user.is_authenticated:
            user.delete()
            return Response(
                {
                    "detail": "User deleted successfully and all associated data have been deleted."
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"detail": "User not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Exception as e:
        return Response(
            {"detail": f"Error deleting user: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def build_threaded_message(message):
    """
    Build a threaded message structure for the given message.
    """
    threaded_message = {
        "message_id": message.message_id,
        "content": message.content,
        "sender": message.sender_id.username,
        "timestamp": message.timestamp,
        "replies": [],
    }

    replies = message.replies.all()
    for reply in replies:
        threaded_message["replies"].append(build_threaded_message(reply))

    return threaded_message
