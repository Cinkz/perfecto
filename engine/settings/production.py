from os.path import abspath, dirname, join


### PATH CONFIGURATION ###
DJANGO_ROOT = dirname(dirname(dirname(abspath(__file__))))

PROJECT_ROOT = dirname(DJANGO_ROOT)

# Security
DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# DEFAULT_DATABASE_NAME = 'perfecto'
# DEFAULT_DATABASE_USERNAME = 'perfecto'
# DEFAULT_DATABASE_PASSWORD = 'kGGB$p@YzwCiv$FkAwDT'
# DEFAULT_DATABASE_HOST = 'rm-uf673l3ey1e3e6173.pg.rds.aliyuncs.com'
# DEFAULT_DATABASE_PORT = '3433'
DEFAULT_DATABASE_NAME = 'perfecto_iapm'
DEFAULT_DATABASE_USERNAME = 'perfecto_iapm'
DEFAULT_DATABASE_PASSWORD = 'kGGB$p@YzwCiv$FkAwDT'
DEFAULT_DATABASE_HOST = 'rm-uf6mpie2gt5v3389k.pg.rds.aliyuncs.com'
DEFAULT_DATABASE_PORT = '3433'

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
        'STATS_FILE': join(PROJECT_ROOT, 'webpack-dist-stats.json'),
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
