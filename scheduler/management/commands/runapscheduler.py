from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util



def obtain_nyse_symbols():
    payload = {"api_token": '61f4b1120141b7.04455674', "fmt": "json"}
    r = requests.get('https://eodhistoricaldata.com/api/exchange-symbol-list/US', params=payload)
    tickers = r.json()
    Symbol.objects.all().delete()
    for ticker in tickers:
        symbol = Symbol(value=ticker["Code"])
        symbol.save()


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
      obtain_nyse_symbols,
      trigger=CronTrigger(minute="*/5"),  # Every 10 seconds
      id="obtain_nyse_symbols",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True,
    )
    scheduler.start()