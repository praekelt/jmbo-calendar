from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point

from jmbo.generic.views import GenericObjectList
from jmbo.view_modifiers import DefaultViewModifier

from jmbo_calendar.models import Event

from atlas.views import location_required


class ObjectList(GenericObjectList):

    def get_extra_context(self, *args, **kwargs):
        request = args[0]
        show_distance = isinstance(request.session['location']['position'], Point)
        return {'title': _('Events'), 'show_distance': show_distance}
        
    def get_queryset(self, *args, **kwargs):
        request = args[0]
        qs = Event.coordinator.upcoming()
        qs = qs.filter(location__country=request.session['location']['city'].country_id)
        position = request.session['location']['position']
        if not isinstance(position, Point):
            position = request.session['location']['city'].coordinates
        qs = qs.distance(position).order_by('distance', 'start')
        return qs

    def get_paginate_by(self, *args, **kwargs):
        return 10

        
_obj_list = ObjectList()

@location_required(override_old=False)
def object_list(*args, **kwargs):
    return _obj_list.__call__(*args, **kwargs)