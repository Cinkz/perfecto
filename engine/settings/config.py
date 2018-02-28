import string, sys

from os.path import abspath, dirname, join, normpath

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


### PATH CONFIGURATION ###
DJANGO_ROOT = dirname(dirname(dirname(abspath(__file__))))

PROJECT_ROOT = dirname(DJANGO_ROOT)

sys.path.append(normpath(join(DJANGO_ROOT, 'apps')))


### APPLICATION CONFIGURATION ###

# Installed apps config
DEFAULT_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
]

PACKAGED_APPS = [
    'qiniustorage',
    'rest_framework',
    'webpack_loader',
]

CUSTOM_APPS = [
    'account',
    'authtoken',
    'channel',
    'dialogue',
    'prototype',
    'script',
    'transaction',
    'utility',
]

INSTALLED_APPS = DEFAULT_APPS + PACKAGED_APPS + CUSTOM_APPS

# Middleware config
DEFAULT_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

PACKAGED_MIDDLEWARE = []

CUSTOM_MIDDLEWARE = [
    'utility.middleware.RequestIPV4Middleware',
]

MIDDLEWARE = DEFAULT_MIDDLEWARE + PACKAGED_MIDDLEWARE + CUSTOM_MIDDLEWARE

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Template config
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(DJANGO_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

# Rest framework config
REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'utility.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'utility.pagination.LinkHeaderLimitOffsetPagination',
    'EXCEPTION_HANDLER': 'utility.exception.handler',
    'UNAUTHENTICATED_USER': None,
}

# Django user model config
AUTH_USER_MODEL = 'account.User'

# Django running environment config
ROOT_URLCONF = 'engine.urls'

WSGI_APPLICATION = 'engine.wsgi.application'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'assets'),
)

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'assets'),
)

DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'
STATICFILES_STORAGE = 'qiniustorage.backends.QiniuStaticStorage'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': join(PROJECT_ROOT, 'web', 'webpack-dist-stats.json'),
    }
}


# Timezone and i18n
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True


### SECURITY CONFIGURATION ###

# Error notification config
ADMINS = (
    ('Chaoyi Du', 'cinkz.d@gmail.com'),
)
MANAGERS = ADMINS

# App config
OAUTH_API_DOMAIN = 'kb.huanmaokuaiban.com/smartsample'

# Secret key
SECRET_FILE = normpath(join(DJANGO_ROOT, 'certificates', 'SECRET.key'))

try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string
        chars = string.ascii_lowercase + string.digits + '!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)

# Certificates
PUBLIC_KEYS = {}
PRIVATE_KEYS = {}
try:
    with open(join(DJANGO_ROOT, 'certificates', 'public', 'auth.pem'), 'rb') as key_file:
        PUBLIC_KEYS['auth'] = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend(),
        )
    with open(join(DJANGO_ROOT, 'certificates', 'private', 'auth.pem'), 'rb') as key_file:
        PRIVATE_KEYS['auth'] = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend(),
        )
except:
    pass

### CONFIGURATION OVERRIDE ###
from production import *

try:
    from local import *
except:
    pass
