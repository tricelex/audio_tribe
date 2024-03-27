import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("audio_tribe")

CELERYBEAT_SCHEDULE = {
    # Test Celery Task ... run every 5 minutes
    # 'test_celery_task': {
    #     'task': 'test_celery_task',
    #     'schedule': crontab(minute='*/2'),
    # },
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE,
    task_serializer="json",
    accept_content=["application/json"],  # Ignore other content
    result_serializer="json",
    timezone="Europe/London",
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
