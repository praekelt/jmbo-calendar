from django.conf.urls import include, url


urlpatterns = [
    url(r"^jmbo/", include("jmbo.urls", namespace="jmbo")),
    url(r"^comments/", include("django_comments.urls")),
    url(r"^calendar/", include("jmbo_calendar.urls", namespace="calendar")),
]
