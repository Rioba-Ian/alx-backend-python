from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow owners or participants of a chat to access it.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        chat = (
            view.get_object()
        )  # Assuming the view has a method to get the chat object
        if not chat:
            return False
        return request.user == chat.owner or request.user in chat.participants.all()

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner or a participant of the chat.
        """
        if hasattr(obj, "owner") and hasattr(obj, "participants"):
            return request.user == obj.owner or request.user in obj.participants.all()
        elif hasattr(obj, "user"):
            # If the object has a user attribute, check if the user is the owner
            return request.user == obj.user
        else:
            return False
