import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secret_santa.settings')

app = Celery('secret_santa', include=['secret_santa.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-every-5-sec': {
        'task': 'secret_santa.tasks.add',
        'schedule': 5.0,
    },
}
app.conf.timezone = 'UTC'
