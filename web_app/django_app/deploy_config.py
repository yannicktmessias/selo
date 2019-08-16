import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===============|| DEPLOYMENT CONFIGURATION ||=============== #

SECRET_KEY = 'w*-p3lw#t+3b96eo)%2a%ye77e1f^o46hk$bg37b5wyu9ua3(s'

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'selo-smped.sa-east-1.elasticbeanstalk.com']

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'djangoappdb',
            'USER': 'djangoappdbuser',
            'PASSWORD': 'password', # input real password here
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')


