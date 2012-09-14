from django.contrib import admin
from django import forms

from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm

from jmbo_calendar.models import Calendar, Event


class EventAdminForm(ModelBaseAdminForm):

    def clean(self, *args, **kwargs):
        data = super(EventAdminForm, self).clean(*args, **kwargs)
        # check that the start is earlier than the end
        if 'start' in data and 'end' in data and \
            data['start'] and data['end'] and data['start'] >= data['end']:
            raise forms.ValidationError('''The event's start date needs
                    to be earlier than its end date''')
        # check that repeat_until is after the end of the first event rep
        if 'repeat_until' in data and 'end' in data and \
            data['repeat_until'] and data['end'] and \
                data['repeat_until'] < data['end'].date():
            raise forms.ValidationError('''An event cannot have a repeat
                    cutoff earlier than the actual event''')

        return data


class EventAdmin(ModelBaseAdmin):
    form = EventAdminForm

    list_display = ('title', 'start', 'end', 'next',
        'repeat', 'repeat_until', 'location')
    list_filter = ('repeat',)


admin.site.register(Calendar, ModelBaseAdmin)
admin.site.register(Event, EventAdmin)
