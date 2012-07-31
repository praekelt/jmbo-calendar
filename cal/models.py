from datetime import datetime, timedelta

from django.db import models

from jmbo.models import ModelBase
from jmbo.managers import DefaultManager

from ckeditor.fields import RichTextField

from atlas.models import Location

from cal.managers import PermittedManager


'''def save_handler_does_not_repeat(entry):
    # raise an error if wrong handler is triggered
    if entry.repeat != 'does_not_repeat':
        raise Exception("In handler 'save_handler_does_not_repeat' for entry \
with repeat set as '%s'" % entry.repeat)

    # delete all entry items related to this entry
    # XXX: yes this is not super efficient, but results in the cleanest code.
    entry.delete_entryitem_set()

    # create a single entryitem linked to entry with provided entry's fields
    entry_item = EntryItem(
        start=entry.start,
        end=entry.end,
        entry=entry,
        content=entry.content
    )
    entry_item.save()

    for calendar in entry.calendars.all():
        entry_item.calendars.add(calendar)


def day_repeater(entry, allowed_days=[0, 1, 2, 3, 4, 5, 6]):
    day = entry.start.date()
    while day <= entry.repeat_until:
        if day.weekday() in allowed_days:
            start = entry.start
            start = start.replace(year=day.year, month=day.month, day=day.day)
            end = start + entry.duration
            entry_item = EntryItem(
                start=start,
                end=end,
                entry=entry,
                content=entry.content
            )
            entry_item.save()

            for calendar in entry.calendars.all():
                entry_item.calendars.add(calendar)

        day = day + timedelta(days=1)


def save_handler_daily(entry):
    # raise an error if wrong handler is triggered
    if entry.repeat != 'daily':
        raise Exception("In handler 'daily' for entry with repeat set as '%s'"\
                % entry.repeat)

    # check for repeat until:
    if not entry.repeat_until:
        raise Exception("Entry should provide repeat_until value for \
'daily' repeat.")

    # delete all entry items related to this entry
    # XXX: yes this is not super efficient, but results in the cleanest code.
    entry.delete_entryitem_set()

    # Create entryitem linked to entry for each day until
    # entry's repeat until value.
    day_repeater(entry, allowed_days=[0, 1, 2, 3, 4, 5, 6])


def save_handler_weekdays(entry):
    # raise an error if wrong handler is triggered
    if entry.repeat != 'weekdays':
        raise Exception("In handler 'weekdays' for entry with repeat set as \
'%s'" % entry.repeat)

    # check for repeat until:
    if not entry.repeat_until:
        raise Exception("Entry should provide repeat_until value for \
'weekdays' repeat.")

    # delete all entry items related to this entry
    # XXX: yes this is not super efficient, but results in the cleanest code.
    entry.delete_entryitem_set()

    # Create entryitem linked to entry for each weekday until entry's
    # repeat until value.
    day_repeater(entry, allowed_days=[0, 1, 2, 3, 4])


def save_handler_weekends(entry):
    # raise an error if wrong handler is triggered
    if entry.repeat != 'weekends':
        raise Exception("In handler 'weekends' for entry with repeat set as \
'%s'" % entry.repeat)

    # check for repeat until:
    if not entry.repeat_until:
        raise Exception("Entry should provide repeat_until value for \
'weekends' repeat.")

    # delete all entry items related to this entry
    # XXX: yes this is not super efficient, but results in the cleanest code.
    entry.delete_entryitem_set()

    # Create entryitem linked to entry for each weekend
    # day until entry's repeat until value.
    day_repeater(entry, allowed_days=[5, 6])


def save_handler_weekly(entry):
    # raise an error if wrong handler is triggered
    if entry.repeat != 'weekly':
        raise Exception("In handler 'weekly' for entry with repeat \
set as '%s'" % entry.repeat)

    # check for repeat until:
    if not entry.repeat_until:
        raise Exception("Entry should provide repeat_until value \
for 'weekly' repeat.")

    # delete all entry items related to this entry
    # XXX: yes this is not super efficient, but results in the cleanest code.
    entry.delete_entryitem_set()

    # Create an entryitem linked to this entry for each week until entry's
    # repeat until value, with the start day being the same for each week.
    day = entry.start.date()
    while day <= entry.repeat_until:
        start = entry.start
        start = start.replace(year=day.year, month=day.month, day=day.day)
        end = start + entry.duration
        entry_item = EntryItem(
            start=start,
            end=end,
            entry=entry,
            content=entry.content
        )
        entry_item.save()

        for calendar in entry.calendars.all():
            entry_item.calendars.add(calendar)

        day = day + timedelta(days=7)


def save_handler_monthly_by_day_of_month(entry):
    # raise an error if wrong handler is triggered
    if entry.repeat != 'monthly_by_day_of_month':
        raise Exception("In handler 'monthly by day of month' for entry \
with repeat set as '%s'" % entry.repeat)

    # check for repeat until:
    if not entry.repeat_until:
        raise Exception("Entry should provide repeat_until value for \
'monthly by day of month' repeat.")

    # delete all entry items related to this entry
    # XXX: yes this is not super efficient, but results in the cleanest code.
    entry.delete_entryitem_set()

    # Create an entryitem linked to entry for each month until entry's
    # repeat until value, with the start day being the same day date
    # of the month for each month.
    day = entry.start.date()
    while day <= entry.repeat_until:
        start = entry.start
        start = start.replace(year=day.year, month=day.month, day=day.day)
        end = start + entry.duration
        entry_item = EntryItem(
            start=start,
            end=end,
            entry=entry,
            content=entry.content
        )
        entry_item.save()

        for calendar in entry.calendars.all():
            entry_item.calendars.add(calendar)
        entry_item.save()

        # get next valid date
        valid_date = False
        i = 1
        while not valid_date:
            try:
                day = day.replace(
                    year=day.year + (day.month + i) / 12,
                    month=(day.month + i) % 12,
                    day=day.day
                )
                valid_date = True
            except ValueError:
                i += 1


class Calendar(ModelBase):
    class Meta():
        verbose_name = "Calendar"
        verbose_name_plural = "Calendars"


class EntryAbstract(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    content = models.ForeignKey(
        'jmbo.ModelBase',
    )

    class Meta():
        abstract = True


class Entry(EntryAbstract):
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
    # XXX: repeat every is a placeholder for now
    repeat_every = models.IntegerField(
        editable=False,
        blank=True,
        null=True,
    )
    repeat_until = models.DateField(
        blank=True,
        null=True,
    )
    calendars = models.ManyToManyField(
        'cal.Calendar',
        related_name='entry_calendar'
    )

    def save(self, *args, **kwargs):
        super(Entry, self).save(*args, **kwargs)
        # create new entry items based on repeat setting
        repeat_handlers = {
            'does_not_repeat': save_handler_does_not_repeat,
            'daily': save_handler_daily,
            'weekdays': save_handler_weekdays,
            'weekends': save_handler_weekends,
            'weekly': save_handler_weekly,
            'monthly_by_day_of_month': save_handler_monthly_by_day_of_month,
        }
        repeat_handlers[self.repeat](self)

    def __unicode__(self):
        return "Entry for %s" % self.content.title

    class Meta():
        verbose_name = "Entry"
        verbose_name_plural = "Entries"

    def delete_entryitem_set(self):
        self.entryitem_set.all().delete()

    @property
    def duration(self):
        return self.end - self.start


class EntryItem(EntryAbstract):
    objects = models.Manager()
    permitted = PermittedManager()

    entry = models.ForeignKey(
        'cal.Entry',
    )
    calendars = models.ManyToManyField(
        'cal.Calendar',
        related_name='entryitem_calendar'
    )

    def __unicode__(self):
        return "Entry Item for %s" % self.content.title

    @property
    def duration(self):
        return self.end - self.start

    class Meta():
        ordering = ('start',)'''


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
    permitted = PermittedManager()
    
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
        help_text='Venue where the event will take place.'
    )    
    content = RichTextField(help_text='Full article detailing this event.')
    
    @property
    def duration(self):
        return end - start
    
    @property
    def next(self):
        now = datetime.now()
        # if the first iteration of the event has not yet ended
        if now < self.end:
            return self.start
        # calculate next repeat of event
        elif self.repeat != 'does_not_repeat' and (self.repeat_until is None or now <= self.repeat_until):
            if now.timetz() < self.end.timetz() or self.duration() > (self.start.replace(hour=23, minute=59, second=59, microsecond=999999) - self.start): 
                date = self._next_repeat(now.date())
            else:
                date = self._next_repeat(now.date().replace(day=now.day + 1))
            
            if date <= self.repeat_until:
                return datetime.combine(date, self.start.timetz())
        return None
    
    # calculate the next repeat - does not take into account repeat_until and assumes the event repeats
    def _next_repeat(self, date):
        if self.repeat == 'daily':
            return date
        elif self.repeat == 'monthly_by_day_of_month':
            date = date.replace(day=self.start.day) if date.day <= self.start.day \
                else date.replace(day=self.start.day, month=date.month + 1)
        else:
            weekday = date.weekday()
            if self.repeat == 'weekdays':
                date = date.replace(day=date.day + 7 - weekday) \
                    if (weekday == 5 or weekday == 6) else date
            elif self.repeat == 'weekends':
                date = date.replace(day=date.day + (5 - weekday)) \
                    if (0 <= weekday <= 4) else date
            else:  # must be weekly
                date = date.replace(day=date.day + (self.start.weekday() - weekday)) \
                    if self.start.weekday() >= weekday else \
                    date.replace(day=date.day + (7 - weekday + self.start.weekday()))
        return date

    class Meta:
        ordering = ('start', )
