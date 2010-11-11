from django.http import HttpResponse
from django.core import cache
from tracker.models import Tracker, make_daily_report

def track(request):
    labels = request.GET.get('labels', False)
    if not labels:
        return HttpResponse("syntax: ?labels=label1|label2")
    tracker = Tracker()
    tracker.incr_labels(labels)
    return HttpResponse("ok")

def report(request):
    make_daily_report()
    return HttpResponse("ok")

