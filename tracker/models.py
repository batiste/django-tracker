from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
import datetime
import re

TTL = 300 # 5 minutes
COLLECT_TIME = 120 # every 2 minutes

QUERY_STRING_VALIDATOR = r'[\w.\-\_\|\+ ]+'


def parse_query(query):
    """
    Can parse "label1|label2" or
              "label.catergory.domid"
    """
    # sanitize
    if not re.match(QUERY_STRING_VALIDATOR, query):
        raise ValueError("Query string is not valid.")

    labels = query.split('|')
    query_list = []
    for label in labels:
        parts = label.split(':')
        if len(parts) == 1:
            query_list.append({'lbl': parts[0]})
        if len(parts) == 2:
            query_list.append({'lbl': parts[0], 'cat': parts[1]})
        if len(parts) == 3:
            query_list.append({'lbl': parts[0], 'cat': parts[1],
                'domid': parts[2]})
        if len(parts) > 3:
            ValueError("Too many dots in your query string.")
    return query_list


class Statistic(models.Model):

    label = models.CharField(max_length=250)
    category = models.CharField(max_length=30, default="None")
    dom_id = models.CharField(max_length=50)
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
        self.labels = cache.get('used_tracker_label_list', {})
        self.changed = False

    def append(self, label):
        if label['lbl'] not in self.labels.keys():
            self.labels[label['lbl']] = label
            self.changed = True
            cache.set('tracker_'+label['lbl'], 0)

    def flush_label(self, label):
        value = cache.get('tracker_'+label, 0)
        cache.set('tracker_'+label, 0)
        return value

    def incr_labels(self, query, save=True):
        labels = parse_query(query)
        for label in labels:
            self.append(label)
            try:
                cache.incr('tracker_'+label['lbl'])
            except ValueError:
                cache.set('tracker_'+label['lbl'], 0)
        if save:
            self.save()

    def save(self):
        if self.changed:
            cache.set('used_tracker_label_list', self.labels)

    def reset_cache(self):
        cache.delete('used_tracker_label_list')


def make_daily_report():
    tracker = Tracker()
    today = datetime.date.today()
    for label, values in tracker.labels.items():

        cat = values.get('cat', "None")
        dom_id = values.get('domid', "None")

        counter = tracker.flush_label(label)
        try:
            s = Statistic.objects.filter(label=label, day=today).latest()
            s.dom_id = dom_id
            s.cat = cat
            s.counter += counter
        except Statistic.DoesNotExist:
            s = Statistic(label=label, category=cat, dom_id=dom_id,
                counter=counter)

        s.save()


