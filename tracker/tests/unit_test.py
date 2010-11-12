import django
from django.conf import settings
from tracker.models import parse_query, Tracker
from tracker.models import Statistic, make_daily_report
from django.test import TestCase

import datetime

class UnitTestCase(TestCase):

    def test_query_string(self):

        query = "label1"
        self.assertEqual(parse_query(query), [{'lbl': 'label1'}])
        query = "label1|label2"
        self.assertEqual(parse_query(query), [{'lbl': 'label1'},
            {'lbl': 'label2'}])

        query = "label1:cat|label2"
        self.assertEqual(parse_query(query), [{'lbl': 'label1', 'cat': 'cat'},
            {'lbl': 'label2'}])

        query = "label1:cat:ele1|label2"
        self.assertEqual(parse_query(query),
            [{'lbl': 'label1', 'cat': 'cat', 'domid': 'ele1'},
            {'lbl': 'label2'}])

    def test_traker(self):

        tracker = Tracker()

        tracker.incr_labels('label1')
        self.assertEqual(tracker.labels, {'label1': {'lbl': 'label1'}})
        tracker.incr_labels('label1')
        self.assertEqual(tracker.flush_label('label1'), 2)
        self.assertEqual(tracker.flush_label('label1'), 0)
        tracker.save()

        tracker = Tracker()
        self.assertEqual(tracker.labels, {'label1': {'lbl': 'label1'}})
        tracker.reset_cache()

    def test_report(self):

        tracker = Tracker()
        tracker.incr_labels('label1:cat1:dom1')
        tracker.incr_labels('label1:cat1:dom1')

        self.assertEqual(Statistic.objects.count(), 0)

        make_daily_report()

        self.assertEqual(tracker.flush_label('label1'), 0)

        self.assertEqual(Statistic.objects.count(), 1)

        stat = Statistic.objects.all()[0]
        self.assertEqual(stat.counter, 2)
        self.assertEqual(stat.category, 'cat1')
        self.assertEqual(stat.dom_id, 'dom1')

        tracker.incr_labels('label1:cat1:dom1')
        tracker.incr_labels('label1:cat1:dom1')

        stat = Statistic.objects.all()[0]
        self.assertEqual(stat.counter, 2)

        make_daily_report()

        stat = Statistic.objects.all()[0]
        self.assertEqual(stat.counter, 4)

        tracker.reset_cache()