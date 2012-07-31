from datetime import datetime, timedelta

from django.db.models.query import Q

from jmbo import managers


class PermittedManager(managers.PermittedManager):
    
    def upcoming(self):
        qs = super(PermittedManager, self).get_query_set()
        now = datetime.now()
        qs.exclude(Q(end__lte=now) & (Q(repeat='does_not_repeat') | Q(repeat_until__lt=now)))
        return qs
