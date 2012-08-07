from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from jmbo.generic.views import GenericObjectList
from jmbo.view_modifiers import DefaultViewModifier

from jmbo_calendar.models import Event


class ObjectList(GenericObjectList):

    def get_extra_context(self, *args, **kwargs):
        return {'title': _('Events'), 'show_distance': True}

    def get_view_modifier(self, request, *args, **kwargs):
        return DefaultViewModifier(request, base_url=reverse('events'), *args, **kwargs)
        
    def get_queryset(self, *args, **kwargs):
        return Event.coordinator.upcoming()

    def get_paginate_by(self, *args, **kwargs):
        return 10

object_list = ObjectList()