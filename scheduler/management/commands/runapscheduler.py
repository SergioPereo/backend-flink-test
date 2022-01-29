from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from apps.business.models import Symbol

import logging

logger = logging.getLogger(__name__)



def obtain_nyse_symbols():
    payload = {"api_token": '61f4b1120141b7.04455674', "fmt": "json"}
    r = requests.get('https://eodhistoricaldata.com/api/exchange-symbol-list/US', params=payload)
    tickers = r.json()
    Symbol.objects.all().delete()
    for ticker in tickers:
        print(ticker["Code"])
        symbol = Symbol(value=ticker["Code"])
        symbol.save()


class Command(BaseCommand):
    help = "Runs APScheduler."
    def handle(self, *args, **options):
        obtain_nyse_symbols()
        """ Intente crear un scheduler pero no encontre la forma de hacer que funcionara, otra implementación sería hacer un sistema aparte para correr el comando cada cierto tiempo, pero eso queda fuera de mis limites de tiempo así que lo hare manualmente
        scheduler = BackgroundScheduler()
        scheduler.add_job(
        obtain_nyse_symbols,
        trigger=CronTrigger(minute="*/5"),
        id="obtain_nyse_symbols",
        max_instances=1,
        replace_existing=True,
        )
        logger.info("Added job 'obtain_nyse_symbols'.")
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
        """