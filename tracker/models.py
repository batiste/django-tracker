from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
import datetime

TTL = 300 # 5 minutes
COLLECT_TIME = 120 # every 2 minutes


class Statistic(models.Model):

    label = models.CharField(max_length=250)
    category = models.CharField(max_length=30, default="None")
    counter = models.IntegerField(default=0)
    day = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _('Statistics')
        ordering = ['-day']
        get_latest_by = "day"

    def __unicode__(self):
        return self.label


class Tracker(object):

    def __init__(self):
        # get the labels that are already used
        self.labels = cache.get('used_tracker_label_list', [])
        self.changed = False

    def append(self, label):
        if label not in self.labels:
            self.labels.append(label)
            self.changed = True
            cache.set('tracker_'+label, 0, TTL)

    def flush_label(self, label):
        value = cache.get('tracker_'+label, 0)
        cache.set('tracker_'+label, 0, TTL)
        return value

    def incr_labels(self, labels):
        labels = labels.split("|")
        for label in labels:
            self.append(label)
            cache.incr('tracker_'+label)

    def save(self):
        if self.changed:
            cache.set('used_tracker_label_list', self.labels)


def make_daily_report():
    tracker = Tracker()
    today = datetime.date.today()
    for label in tracker.labels:
        try:
            s = Statistic.objects.filter(label=label).latest()
            cat = s.category
        except Statistic.DoesNotExist:
            cat = "None"

        counter = tracker.flush_label(label)
        try:
            s = Statistic.objects.filter(label=label, day=today).latest()
            s.counter += counter
        except Statistic.DoesNotExist:
            s = Statistic(label=label, category=cat, counter=counter)

        s.save()


