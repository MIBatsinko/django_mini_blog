import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miniblog.settings')

celery_app = Celery('miniblog')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
