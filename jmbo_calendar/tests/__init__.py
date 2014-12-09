from datetime import datetime

from django.test import TestCase as BaseTestCase
from django.test.client import Client as BaseClient, RequestFactory
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from django.utils import timezone
from django.utils.timezone import timedelta
from django.contrib.sites.models import Site

from jmbo_calendar.models import Calendar, Event


class TestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.request = RequestFactory()
        cls.client = BaseClient()

        # Editor
        cls.editor, dc = User.objects.get_or_create(
            username='editor',
            email='editor@test.com'
        )
        cls.editor.set_password("password")
        cls.editor.save()

        # Event
        obj, dc = Event.objects.get_or_create(
            title='Event',
            start=timezone.now(),
            end=timezone.now() + timezone.timedelta(days=1),
            content="Event content",
            owner=cls.editor, state='published',
        )
        obj.sites = [1]
        obj.save()
        cls.event = obj

    def setUp(self):
        self.dt = timezone.now()

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
        # event that has an upcoming repeat_until date,
        # but won't have another repetition
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
        self.make_published_events()
        titles = Event.coordinator.upcoming().values_list('title', flat=True)
        # check that only e1 and e3 are in upcoming query set
        self.assertTrue('e1' in titles)
        self.assertTrue('e2' not in titles)
        self.assertTrue('e3' in titles)
        self.assertTrue('e4' not in titles)
        self.assertTrue('e5' not in titles)

    def test_no_repeat(self):
        e = Event.objects.create(
            title='e',
            start=self.dt + timedelta(days=1),
            end=self.dt + timedelta(days=1, hours=1),
        )
        # check that event is upcoming
        self.assertEqual(e.next, e.start)
        # check that next returns None when event is over
        e.start = self.dt - timedelta(days=1)
        e.end = self.dt - timedelta(days=1, hours=-1)
        e.save()
        self.assertEqual(e.next, None)

    def test_daily_repeat(self):
        tomorrow = self.dt + timedelta(days=1)
        e = Event.objects.create(
            title='e',
            start=self.dt - timedelta(days=1),
            end=self.dt - timedelta(days=1, hours=-1),
            repeat='daily',
            repeat_until=tomorrow.date()
        )
        # check that repeat_until is calculated correctly on save()
        self.assertEqual(tomorrow.date(), e.repeat_until)
        # check that next repetition is today at event start time
        self.assertEqual(e.next, datetime.combine(self.dt.date(),
                e.start.timetz()))

    def test_weekly_repeat(self):
        e = Event.objects.create(
            title='e',
            start=self.dt - timedelta(days=1),
            end=self.dt - timedelta(days=1, hours=-1),
            repeat='weekly',
            repeat_until=(self.dt + timedelta(days=1)).date()
        )
        # check that repeat_until is calculated correctly on save()
        self.assertEqual(e.repeat_until, e.start.date())
        # check that there is no next repeat (repeat_until is too early)
        self.assertEqual(e.next, None)
        # check that next repetition is start + 1 week
        e.repeat_until = (self.dt + timedelta(days=7)).date()
        e.save()
        self.assertEqual(e.next, e.start + timedelta(days=7))
        # check that repeat_until is calculated correctly on save()
        self.assertEqual(e.repeat_until, e.start.date() + timedelta(days=7))

    def test_weekend_repeat(self):
        final_repeat = (self.dt + timedelta(days=6)).date()
        e = Event.objects.create(
            title='e',
            start=self.dt - timedelta(days=1),
            end=self.dt - timedelta(days=1, hours=-1),
            repeat='weekends',
            repeat_until=final_repeat
        )
        # check that repeat_until is calculated correctly on save()
        if 5 <= final_repeat.weekday() <= 6:
            self.assertEqual(e.repeat_until, final_repeat)
        else:
            self.assertEqual(e.repeat_until, final_repeat -
                    timedelta(days=final_repeat.weekday() + 1))
        # check that next is caculated correctly
        self.assertTrue(5 <= e.next.weekday() <= 6)

    def test_weekday_repeat(self):
        pass

    def test_monthly_repeat(self):
        pass

    def test_event_detail(self):
        response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.failUnless("Event content" in response.content)

    def test_event_list_item_thumbnail(self):
        t = loader.get_template(
            "jmbo_calendar/inclusion_tags/event_list_item_thumbnail.html"
        )
        context = RequestContext(self.request)
        context["object"] = self.event
        html = t.render(context)
        self.failUnless(
            """<a href="/calendar/event/event/">Event</a>""" in html
        )
