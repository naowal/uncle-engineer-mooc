from .base import *

DEBUG = False

ADMINS = (
    ('Naowal S', 'naowalzaza@gmail.com'),)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'educa',
        'USER': 'educa',
        'PASSWORD': 'educa',
    }
}