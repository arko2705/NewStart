from __future__ import absolute_import,unicode_literals  ##For compatibility of versions.
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewStart.settings')  #NewStart is the inner newstart,inside which settings is present

app = Celery('NewStart')  ##again inside which celery.py is
app.conf.enable_utc=False #setting the default timezone utc as false as we are using timezone asia kolkata
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY') #This line tells Celery to load its configuration from Django’s settings (in settings.py) but only variables prefixed with CELERY_ (e.g., CELERY_BROKER_URL).
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'
# Using a string here means the worker doesn't have to serialize

app.autodiscover_tasks()                        # Load task modules from all registered Django apps.
app.conf.broker_transport_options = {'visibility_timeout': 1800}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')