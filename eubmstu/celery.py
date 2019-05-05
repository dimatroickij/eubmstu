import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eubmstu.settings')

app = Celery('eubmstu')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()