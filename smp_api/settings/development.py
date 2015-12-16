from smp_api.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ilr_akb-3#6m!!9!=43c&uc%0q$ic0wsxo_y(n@3u4%&gtpqig'

INSTALLED_APPS += [
    'debug_toolbar',
]

