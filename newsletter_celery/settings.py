BROKER_URL = 'redis_stuff'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.
CELERY_RESULT_BACKEND = 'redis_stuff'  # same as BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('app.tasks', )

# # celery-beat configuration
# from celery.schedules import crontab
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'activate_emails': {
        'task': 'app.tasks.activate_emails',
        # 'schedule': crontab(minute='*/1'),# minute=0, hour=16, day_of_week='fri'),
        'schedule': timedelta(seconds=10),
    },
}