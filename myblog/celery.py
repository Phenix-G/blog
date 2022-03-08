import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings.development')

app = Celery('myblog', broker='redis://localhost:6379/5', backend='redis://localhost:6379/6')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('myblog.settings.development', namespace='CELERY')
app.autodiscover_tasks()

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'autosc': {
            'task': 'marvel.tasks.auto_sc',
            'schedule': timedelta(seconds=3),
        },
    }
)


