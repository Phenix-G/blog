import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings.development')

app = Celery('myblog')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('myblog.settings.development', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'base_marvel_info': {
    #     'task': 'base_marvel_info',
    #     # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
    #     'schedule': 10,
    # },
    'hero': {
        'task': 'hero',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'schedule': 10,
    }
}
