from datetime import datetime, timedelta
import calendar

from django.db import models

from jmbo.models import ModelBase
from jmbo.managers import DefaultManager

from ckeditor.fields import RichTextField

from atlas.models import Location

from cal.managers import PermittedManager


class Calendar(ModelBase):

    class Meta:
        verbose_name = "Calendar"
        verbose_name_plural = "Calendars"


class Event(ModelBase):
    parent_ptr = models.OneToOneField(
        ModelBase,
        primary_key=True,
        parent_link=True,
        related_name='+'
    )

    objects = DefaultManager()
    coordinator = PermittedManager()

    start = models.DateTimeField()
    end = models.DateTimeField()
    repeat = models.CharField(
        max_length=64,
        choices=(
            ('does_not_repeat', 'Does Not Repeat'),
            ('daily', 'Daily'),
            ('weekdays', 'Weekdays'),
            ('weekends', 'Weekends'),
            ('weekly', 'Weekly'),
            ('monthly_by_day_of_month', 'Monthly By Day Of Month'),
        ),
        default='does_not_repeat',
    )
    repeat_until = models.DateField(
        blank=True,
        null=True,
    )
    calendars = models.ManyToManyField(
        'cal.Calendar',
        blank=True,
        null=True,
        related_name='event_calendar',
    )
    venue = models.ForeignKey(
        Location,
        help_text='Venue where the event will take place.',
        blank=True,
        null=True,
    )
    content = RichTextField(help_text='Full article detailing this event.')

    @property
    def duration(self):
        return self.end - self.start

    @property
    def next(self):
        now = datetime.now()
        # if the first iteration of the event has not yet ended
        if now < self.end:
            return self.start
        # calculate next repeat of event
        elif self.repeat != 'does_not_repeat' and \
                (self.repeat_until is None or now.date() <= self.repeat_until):
            if now.timetz() < self.end.timetz() or self.duration > \
                    (self.start.replace(hour=23, minute=59, second=59,
                    microsecond=999999) - self.start):
                date = self._next_repeat(now.date())
            else:
                date = self._next_repeat(now.date() + timedelta(days=1))

            if date <= self.repeat_until:
                return datetime.combine(date, self.start.timetz())
        return None

    # calculate the next repeat, ignores repeat_until and assumes repetition
    def _next_repeat(self, date):
        if self.repeat == 'daily':
            return date
        elif self.repeat == 'monthly_by_day_of_month':
            if date.day > self.start.day:  # skip to next month
                date = date.replace(day=1, month=(date.month + 1) % 12,
                        year=date.year + math.floor((date.month + 1) / 12))

            if self.start.day > calendar.monthrange(date.year, date.month)[1]:
                date = date.replace(day=calendar.monthrange(date.year,
                        date.month)[1])
            else:
                date = date.replace(day=self.start.day)
        else:
            weekday = date.weekday()
            if self.repeat == 'weekdays':
                date = date + timedelta(days=7 - weekday) \
                    if (weekday == 5 or weekday == 6) else date
            elif self.repeat == 'weekends':
                date = date + timedelta(days=5 - weekday) \
                    if (0 <= weekday <= 4) else date
            else:  # must be weekly
                date = date + timedelta(days=self.start.weekday() - weekday) \
                    if self.start.weekday() >= weekday else \
                    date + timedelta(days=7 - weekday + self.start.weekday())
        return date

    def save(self, *args, **kwargs):
        # set repeat_until to the exact date of the final repetition
        if self.repeat != 'does_not_repeat':
            if self.repeat_until is not None:
                next = self._next_repeat(self.repeat_until)
                if next > self.repeat_until:
                    if self.repeat == 'daily':
                        raise ValueError('This should not be possible')
                    elif self.repeat == 'weekly':
                        self.repeat_until = next - timedelta(days=7)
                    elif self.repeat == 'weekdays':
                        self.repeat_until = self.repeat_until - \
                            timedelta(days=self.repeat_until.weekday() - 4)
                    elif self.repeat == 'weekends':
                        self.repeat_until = self.repeat_until - \
                            timedelta(days=self.repeat_until.weekday() + 1)
                    else:  # must be 'monthly_by_day_of_month'
                        self.repeat_until = next - timedelta(days=
                                calendar.monthrange(self.repeat_until.year,
                                self.repeat_until.month)[1])
                elif next < self.repeat_until:
                    raise ValueError('''The repeat_until date is too early
                            and the event will never be repeated.''')
        else:
            self.repeat_until = None

        super(Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ('start', )
