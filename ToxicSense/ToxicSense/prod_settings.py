import os

from ToxicSense.settings import *


ALLOWED_HOSTS = [
    'www.toxicsense.com',
    'toxicsense.com',
    'first-env.jchmcupa3h.us-east-1.elasticbeanstalk.com',
]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/prod-static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'prod-static')
