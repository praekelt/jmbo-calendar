import random
import math
import simplejson
from datetime import timedelta

from django.utils import timezone
from django.contrib.sites.models import Site

from atlas.models import Location

from jmbo_calendar.models import Event


'''
Generates events with randomly assigned locations - first generate locations.
'''
def generate():
    objects = []
    now = timezone.now()
    repeat_choices = Event._meta.get_field_by_name('repeat')[0].choices
    site_id = Site.objects.all()[0].id
    for i in range(1, 101):
        start = now + timedelta(days=math.ceil(random.random()*90))
        end = (start + timedelta(hours=math.ceil(random.random()*48))) \
                .strftime('%Y-%m-%d %H:%M:%S')
        start = start.strftime('%Y-%m-%d %H:%M:%S')
        obj = {
            'model': 'jmbo_calendar.Event',
            'fields': {
                'location': {'model': 'atlas.Location', 'fields': {'id': int(Location.objects.order_by('?')[0].id)}},
                'title': 'Event_%d' % i,
                'start': start,
                'end': end,
                'repeat': repeat_choices[int(random.random() * len(repeat_choices))][0],
                'content': 'Event_%d content' % i,
                'sites': [int(site_id)],
            }
        }
        objects.append(obj)

    return objects