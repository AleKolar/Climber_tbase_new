from .settings import *


DEBUG = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tbase',
        'USER': os.getenv('FSTR_DB_LOGIN'),
        'PASSWORD': os.getenv('FSTR_DB_PASS'),
        'HOST': os.getenv('FSTR_DB_HOST'),
        'PORT': os.getenv('FSTR_DB_PORT'),
        'OPTIONS': {
            'options': '-c client_encoding=UTF8 -c search_path=public'
        },
    }
}


MIGRATION_MODULES = {app: 'tbase.test_migrations' for app in INSTALLED_APPS}