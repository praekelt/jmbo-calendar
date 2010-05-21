import calendar
from datetime import datetime, timedelta

from pagemenu.items import GetItem
from pagemenu.pagemenus import PageMenu

class EntryByWeekdayItem(GetItem):
    def __init__(self, request, title, get, date, default):
        self.date=date
        super(EntryByWeekdayItem, self).__init__(request=request, title=title, get=get, default=default)

    def action(self, queryset):
        return queryset.by_date(self.date)

class EntriesByWeekdaysPageMenu(PageMenu):
    def __init__(self, queryset, request):
        self.items = []
        now = datetime.now().date()
        
        day_names = [name for name in calendar.day_abbr]
        current_day = day_names[now.weekday()]

        
        dates_by_day = {}
        date = now
        while date < now + timedelta(days=7):
            dates_by_day[day_names[date.weekday()]] = date
            date = date + timedelta(days=1)

        for name in day_names:
            self.items.append(EntryByWeekdayItem(
                request=request,
                title=name,
                get={'name': 'day', 'value': name},
                date=dates_by_day[name],
                default=current_day==name,
            ))
            
        super(EntriesByWeekdaysPageMenu, self).__init__(queryset, request)
