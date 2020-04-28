from django.db.models import Q
from django.utils import timezone


def get_active_campaigns(campaigns):
    now = timezone.now()
    not_yet_started = Q(starts_at__gt=now)
    already_ended = Q(ends_at__lte=now)
    return campaigns.exclude(not_yet_started | already_ended)
