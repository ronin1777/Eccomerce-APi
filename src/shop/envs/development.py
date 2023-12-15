from .common import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
   'daphne',
   'drf_spectacular',
] + INSTALLED_APPS

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop',
        'USER': 'comiser',
        'PASSWORD': 'Hosein67',
        'HOST': 'db',
        'PORT': '5432',
    },
    'test': {
        # Separate test database configuration
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'unittest',
        'HOST': 'localhost',
        'PORT': '5432',

}
}

# TEST = {
#     'NAME': 'test',
# }
