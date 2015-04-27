from django.conf.urls import patterns, url

from atlas.views import location_required

from jmbo.views import ObjectDetail
from jmbo_calendar.views import ObjectList


urlpatterns = patterns('',

    url(
        r'^events/$',
        location_required(ObjectList.as_view()),
        name='events'
    ),

    url(
        r'^event/(?P<slug>[\w-]+)/$',
        ObjectDetail.as_view(),
        name='event_object_detail'
    ),

)
