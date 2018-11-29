from ToxicSense.settings import *


ENABLE_CELERY = True
CELERY_BROKER_URL = 'pyamqp://guest@localhost//'
CELERY_BROKER_TRANSPORT_OPTIONS = {"max_retries": 3, "interval_start": 0, "interval_step": 0.2, "interval_max": 0.5}
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'collect_top_trends': {
        'task': 'clientapp.tasks.collect_top_trends',
        'schedule': datetime.timedelta(minutes=15)
    },
}
