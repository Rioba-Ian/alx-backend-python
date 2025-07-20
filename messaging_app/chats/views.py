from django.shortcuts import render
from rest_framework import viewsets
from .models import CustomUser, Conversation, Message
from .serializers import CustomUserSerializer, ConversationSerializer, MessageSerializer

# Create your views here.


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender_id=self.request.user)
