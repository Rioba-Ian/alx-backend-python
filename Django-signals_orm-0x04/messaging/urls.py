from django.urls import path, include
from rest_framework import routers
from .views import (
    ConversationViewSet,
    MessageViewSet,
    UnreadMessagesView,
    NotificationViewSet,
    delete_user,
)


router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"history", NotificationViewSet, basename="notification")


urlpatterns = [
    path("", include(router.urls)),
    path("delete-user/", delete_user.as_view(), name="delete_user"),
    path(
        "messages/unread/",
        UnreadMessagesView.as_view(),
        name="unread_messages",
    ),
]
