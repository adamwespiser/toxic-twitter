import os

from ToxicSense.settings import *


ALLOWED_HOSTS = [
    'django-toxic-sense-dev.us-east-1.elasticbeanstalk.com',
    'first-env.7ys2prfhhm.us-east-1.elasticbeanstalk.com',
    'www.toxicsense.com',
    'toxicsense.com'
]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/prod-static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'prod-static')
