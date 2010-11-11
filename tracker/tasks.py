from datetime import timedelta
from celery.decorators import task, periodic_task
from tracker.models import make_daily_report

@periodic_task(run_every=timedelta(seconds=120))
def collect_statistic():
    make_daily_report()

