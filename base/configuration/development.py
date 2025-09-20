"""
To switch between development and production environments:
Set the DJANGO_SETTINGS_MODULE variable in both wsgi.py, asgi.py and manage.py
to point to the correct settings file, e.g. 'myproject.settings.production'

Example for production:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings.production')

Example for development:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings.development')
"""

from .config import *
from decouple import config, Csv
import secrets

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Leave empty in .env if youre sticking to sqlite
DB_ENGINE = config('DB_ENGINE', default='sqlite')

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': 'localhost',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "gateway.auth.APIKeyAuthenticationMiddleware",
    ],
}

INTERNAL_IPS = [
    "127.0.0.1",
]
