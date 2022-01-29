from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from apps.business.models import Symbol
import requests
import sys

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def obtain_nyse_symbols():
    payload = {"api_token": '61f4b1120141b7.04455674', "fmt": "json"}
    r = requests.get('https://eodhistoricaldata.com/api/exchange-symbol-list/US', params=payload))
    tickers = r.json()
    Symbol.objects.all().delete()
    for ticker in tickers:
        symbol = Symbol(value=ticker["Code"])
        symbol.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    scheduler.add_job(obtain_nyse_symbols, 'interval', hours=24, name='clean_accounts', jobstore='default')
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)