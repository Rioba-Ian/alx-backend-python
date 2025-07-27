from .models import Message
import django_filters


class MessageFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    sender = django_filters.NumberFilter(field_name="sender__id")
    recipient = django_filters.NumberFilter(field_name="recipient__id")

    class Meta:
        model = Message
        fields = ["created_at", "sender", "recipient"]
