from smp_api.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

import os
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Corsheaders Config
# https://github.com/ottoyiu/django-cors-headers/

CORS_ORIGIN_WHITELIST = (
    'sarahquigley.net',
)
