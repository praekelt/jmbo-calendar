from django.conf.urls.defaults import patterns, include


urlpatterns = patterns(
    '',
    (r'^jmbo/', include('jmbo.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^calendar/', include('jmbo_calendar.urls')),
)
