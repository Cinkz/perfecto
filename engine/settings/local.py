from os.path import abspath, dirname, join


### PATH CONFIGURATION ###
DJANGO_ROOT = dirname(dirname(dirname(abspath(__file__))))

PROJECT_ROOT = dirname(DJANGO_ROOT)

# Security
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
DEFAULT_DATABASE_NAME = 'perfecto'
DEFAULT_DATABASE_USERNAME = 'perfecto'
DEFAULT_DATABASE_PASSWORD = '169617'
DEFAULT_DATABASE_HOST = ''
DEFAULT_DATABASE_PORT = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DEFAULT_DATABASE_NAME,
        'USER': DEFAULT_DATABASE_USERNAME,
        'PASSWORD': DEFAULT_DATABASE_PASSWORD,
        'HOST': DEFAULT_DATABASE_HOST,
        'PORT': DEFAULT_DATABASE_PORT,
    }
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': join(PROJECT_ROOT, 'webpack-dev-stats.json'),
    }
}

# Qiniu Config
QINIU_ACCESS_KEY = '7cehK4Vw6ohmV0RkV0hSWuD-yvTssI59GvVe1wG_'
QINIU_SECRET_KEY = 'Jvwa0aE4Hr58SISXDCdUmZI4DAt96RchKgInSrUW'
QINIU_BUCKET_NAME = 'perfecto'
QINIU_BUCKET_DOMAIN = 'assets.dzfaners.com'
QINIU_SECURE_URL = True

# Ping++
PINGPP_APP_ID = 'app_Oa1S8GvznzTCTyTu'
PINGPP_API_KEY = 'sk_live_CYYECLbulCAL2yi6cpDmaKWw'
