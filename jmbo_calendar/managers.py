from datetime import datetime, timedelta

from django.db.models.query import Q
from django.utils import timezone

from jmbo import managers


class CoordinatorManager(managers.PermittedManager):

    def upcoming(self):
        qs = super(CoordinatorManager, self).get_query_set()
        now = timezone.now()
        return qs.exclude(Q(end__lte=now) &
                (Q(repeat='does_not_repeat') | (~Q(repeat_until=None) &
                Q(repeat_until__lt=now.date()))))
