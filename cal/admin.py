from django.contrib import admin

from jmbo.admin import ModelBaseAdmin

from cal.models import Calendar, Event


class EventAdmin(ModelBaseAdmin):
    list_display = ('title', 'start', 'end', 'next',
        'repeat', 'repeat_until', 'venue')
    list_filter = ('repeat',)


admin.site.register(Calendar, ModelBaseAdmin)
admin.site.register(Event, EventAdmin)
