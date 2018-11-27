import os

import requests

from django.core.exceptions import ImproperlyConfigured

from ToxicSense.settings import *

 
def get_ec2_hostname():
    try:
        ipconfig = 'http://169.254.169.254/latest/meta-data/local-ipv4'
        return requests.get(ipconfig, timeout=10).text
    except Exception:
        error = 'You have to be running on AWS to use AWS settings'
        raise ImproperlyConfigured(error)
 

ALLOWED_HOSTS = [
    get_ec2_hostname(),
    '127.0.0.1',
    'localhost',
    '.amazonaws.com',
    '.elasticbeanstalk.com',
    'www.toxicsense.com',
    'toxicsense.com',
    'first-env.jchmcupa3h.us-east-1.elasticbeanstalk.com',
]

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/prod-static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'prod-static')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
