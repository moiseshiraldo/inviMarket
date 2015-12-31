# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
	'USER': '',
	'PASSWORD': '',
	'HOST': '',
	'PORT': '',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = ''

CACHES = {
    'default': {
        'BACKEND': 'django_elasticache.memcached.ElastiCache',
        'LOCATION': '',
    }
}

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = 'invimarket'
DEFAULT_FILE_STORAGE = 'inviMarket.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'inviMarket.s3utils.StaticRootS3BotoStorage'

GOOGLE_ANALYTICS_KEY = ''
GS_EMAIL = ''
GS_CREDENTIALS = ''