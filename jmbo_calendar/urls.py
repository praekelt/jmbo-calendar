from django.conf.urls.defaults import patterns, url

from jmbo_calendar.views import object_list


urlpatterns = patterns('',
    
    url(
        r'^events/$',
        object_list,
        name='events'
    ),
    
    url(
        r'^event/(?P<slug>[\w-]+)/$', 
        'jmbo.views.object_detail',
        {},
        name='event_object_detail'
    ),

)
