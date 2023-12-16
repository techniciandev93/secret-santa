import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secret_santa.settings')

app = Celery('secret_santa', include=['secret_santa.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    #for test only
    'check-every-10-sec': {
        'task': 'secret_santa.tasks.get_sortition',
        'schedule': 10.0,
    },
}

app.conf.beat_schedule = {
    # Every day
    'every-day': {
        'task': 'secret_santa.tasks.get_sortition',
        'schedule': crontab(minute=0, hour=0),
    },
}
