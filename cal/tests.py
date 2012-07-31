import unittest
from datetime import datetime, timedelta

from django.test import TestCase
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models

from cal.models import Calendar, Event

class CalTestCase(TestCase):

    def setUp(self):
        self.dt = datetime.now()
        self.make_published_events()
    
    def make_published_events(self):
        hour1 = timedelta(hours=1)
        day1 = timedelta(days=1)
        day2 = timedelta(days=2)
        # upcoming event (no repeat)
        e1 = Event.objects.create(
            title="e1",
            start=self.dt + day1,
            end=self.dt + day2,
        )
        # event that has happened (no repeat)
        e2 = Event.objects.create(
            title="e2",
            start=self.dt - day1,
            end=self.dt - hour1,
        )
        # event that is going to be repeated
        e3 = Event.objects.create(
            title="e3",
            start=self.dt - day1,
            end=self.dt - hour1,
            repeat="daily",
        )
        # event that is past its repeat_until date
        e4 = Event.objects.create(
            title="e4",
            start=self.dt - day2,
            end=self.dt - day2 + hour1,
            repeat="weekly",
            repeat_until=self.dt - day1
        )
        # event that has an upcoming repeat_until date, but won't have another repetition
        e5 = Event.objects.create(
            title="e5",
            start=self.dt - day2,
            end=self.dt - day2 + hour1,
            repeat="weekly",
            repeat_until=self.dt + day1
        )
        
        # publish all the events
        site = Site.objects.all()[0]
        for e in (e1, e2, e3, e4, e5):
            e.sites.add(site)
            e.publish()

    def test_upcoming(self):
        titles = Event.coordinator.upcoming().values_list('title', flat=True)
        # check that only e1 and e3 are in upcoming query set
        self.assertTrue('e1' in titles)
        self.assertTrue('e3' in titles)
        self.assertTrue(len(titles) == 2)