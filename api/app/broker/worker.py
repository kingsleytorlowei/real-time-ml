import os 
from os import path
import time 
from celery import Celery

app = Celery('tasks', include=['broker.tasks'])
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
