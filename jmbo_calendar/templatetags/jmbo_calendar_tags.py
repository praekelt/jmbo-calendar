from datetime import datetime, timedelta

from django import template
from django.utils.translation import ugettext as _
from django.utils import timezone


register = template.Library()


@register.filter
def scheduled_for(event_obj):
    next = event_obj.next
    if next:
        now = timezone.now()
        if next.date() == now.date():
            return next.strftime("today at %H:%M (%Z)")
        elif next.day == now.day + 1:
            return next.strftime("tomorrow at %H:%M (%Z)")
        else:
            return next.strftime("%d %b at %H:%M (%Z)")
    return ''