from django.conf.urls import patterns, url


from jmbo import USE_GIS
from jmbo.views import ObjectDetail
from jmbo_calendar.views import ObjectList


if USE_GIS:
    from atlas.views import location_required


urlpatterns = patterns('',

    url(
        r'^events/$',
        USE_GIS and location_required(ObjectList.as_view()) or ObjectList.as_view(),
        name='events'
    ),

    url(
        r'^event/(?P<slug>[\w-]+)/$',
        ObjectDetail.as_view(),
        name='event_object_detail'
    ),

)
