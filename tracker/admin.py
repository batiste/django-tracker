from tracker.models import Statistic
from django.contrib import admin


class StatisticAdmin(admin.ModelAdmin):

    list_display = ('label', 'category', 'counter', 'day', 'dom_id')
    list_filter = ('day', 'category', 'label')


admin.site.register(Statistic, StatisticAdmin)

