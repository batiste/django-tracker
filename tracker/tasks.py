from datetime import timedelta
from celery.decorators import task, periodic_task
from tracker.models import make_daily_report, COLLECT_TIME

@periodic_task(run_every=timedelta(seconds=COLLECT_TIME))
def collect_statistic():
    make_daily_report()

