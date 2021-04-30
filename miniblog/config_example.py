SECRET_KEY = ''
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'miniblog',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STRIPE_PUBLISHABLE_KEY = ''
STRIPE_SECRET_KEY = ''
STRIPE_ENDPOINT_SECRET = ''
STRIPE_PRICE_ID = ''
