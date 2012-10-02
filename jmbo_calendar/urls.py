from django.conf.urls.defaults import patterns, url

from jmbo_calendar.views import object_list


urlpatterns = patterns('',
    # events url
    url(
        r'^events/$',
        object_list,
        name='events'
    ),
)