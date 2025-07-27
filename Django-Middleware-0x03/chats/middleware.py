import logging

from django.http import HttpResponseForbidden
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware to log request details and check for rate limiting.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = {}

    def __call__(self, request):
        # Log the request details
        logger.info(f"Request Method: {request.method}, Path: {request.path}")

        # Rate limiting logic
        client_ip = request.META.get("REMOTE_ADDR")
        current_time = datetime.now()

        if client_ip not in self.request_log:
            self.request_log[client_ip] = []

        # Clean up old requests
        self.request_log[client_ip] = [
            timestamp
            for timestamp in self.request_log[client_ip]
            if timestamp > current_time - timedelta(seconds=60)
        ]

        if len(self.request_log[client_ip]) >= 100:
            return HttpResponseForbidden("Rate limit exceeded. Try again later.")

        # Log the current request time
        self.request_log[client_ip].append(current_time)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to certain times of the day.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = datetime.strptime("08:00", "%H:%M").time()
        end_time = datetime.strptime("18:00", "%H:%M").time()

        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden(
                "Access is restricted outside of business hours."
            )

        response = self.get_response(request)
        return response


class RolePermissionMiddleware:
    """
    Middleware to check user roles and permissions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseForbidden(
                "You must be logged in to access this resource."
            )

        # Example role check
        if not user.has_perm("chats.view_chat"):
            return HttpResponseForbidden(
                "You do not have permission to view this chat."
            )

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to filter offensive language in chat messages.
    """

    OFFENSIVE_WORDS = {"badword1", "badword2", "badword3"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and "message" in request.POST:
            message = request.POST["message"]
            if any(word in message.lower() for word in self.OFFENSIVE_WORDS):
                return HttpResponseForbidden(
                    "Your message contains offensive language."
                )

        response = self.get_response(request)
        return response
