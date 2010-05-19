from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import Q

class EntryItemQuerySet(models.query.QuerySet):
    def by_model(self, model):
        """
        Should only return entry items for content of the provided model.
        """
        content_type = ContentType.objects.get_for_model(model)
        return self.filter(content__content_type__exact=content_type)

    def now(self):
        """
        Filters for currently active entry items
        """
        now = datetime.now()
        return self.filter(start__lt=now, end__gt=now)

    def by_date(self, date):
        start = datetime(date.year, date.month, date.day)
        end = start + timedelta(days=1)
        
        # to force inclusion offset start and end by 1 second
        # start = start + timedelta(seconds=1)
        # end = end - timedelta(seconds=1)

        return self.by_range(start, end)
    
    def by_range(self, start, end):
        return self.exclude(start__gte=end).exclude(end__lte=start)

class PermittedManager(models.Manager):
    def get_query_set(self):
        # get base queryset
        queryset = EntryItemQuerySet(self.model)
        
        # exclude entries for unpublished calendars
        queryset = queryset.exclude(calendars__state='unpublished')
        
        # exclude entries for unpublished content
        queryset = queryset.exclude(content__state='unpublished')

        # exclude objects in staging state if not in staging mode (settings.STAGING = False)
        if not getattr(settings, 'STAGING', False):
            # exclude entries for staging calendars
            queryset = queryset.exclude(calendars__state='staging')
        
            # exclude entries for staging content
            queryset = queryset.exclude(content__state='staging')

        # filter calendar for current site 
        queryset = queryset.filter(calendars__sites__id__exact=settings.SITE_ID)
        
        # filter content for current site 
        queryset = queryset.filter(content__sites__id__exact=settings.SITE_ID)
        
        return queryset

    def by_model(self, model):
        return self.get_query_set().by_model(model)

    def now(self):
        return self.get_query_set().now()

    def by_date(self, date):
        return self.get_query_set().by_date(date)
    
    def by_range(self, start, end):
        return self.get_query_set().by_range(start, end)