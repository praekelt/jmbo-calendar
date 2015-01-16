from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point

from jmbo.views import ObjectList

from jmbo_calendar.models import Event


class ObjectList(ObjectList):

    def get_context_data(self, **kwargs):
        context = super(ObjectList, self).get_context_data(**kwargs)
        show_distance = isinstance(self.request.session['location']['position'], Point)
        context["title"] = _("Events")
        context["show_distance"] = show_distance
        return context

    def get_queryset(self):
        request = args[0]
        qs = Event.coordinator.upcoming()
        qs = qs.filter(location__country=self.request.session['location']['city'].country_id)
        position = self.request.session['location']['position']
        if not isinstance(position, Point):
            position = self.request.session['location']['city'].coordinates
        qs = qs.distance(position).order_by('distance', 'start')
        return qs

    def get_paginate_by(self, *args, **kwargs):
        # todo: needs work in Jmbo to work
        return 10
