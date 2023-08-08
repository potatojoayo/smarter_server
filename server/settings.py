"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import logging
import logging.handlers
from datetime import timedelta, datetime
from pathlib import Path
import os
import firebase_admin
from celery.schedules import crontab
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

default_firebase_cred = credentials.Certificate(
    os.path.join(BASE_DIR, 'firebase.json'))
default_app = firebase_admin.initialize_app(default_firebase_cred)
parents_firebase_cred = credentials.Certificate(
    os.path.join(BASE_DIR, 'firebase_parents.json'))
parents_app = firebase_admin.initialize_app(
    parents_firebase_cred, name='parents')

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pxa!e-8-!g@7tos=0$5&%ng!$8jxla4*-u1$jy3m=6+#zv2-pa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ALLOWED_ORIGINS = [
#    "http://localhost:5001",
#    "http://localhost:5173",
#    "https://www.admin.ksmarter.shop"
# ]
#
# CORS_ORIGIN_WHITELIST = [
#    "http://localhost:5001",
#    "http://localhost:5173",
#    "https://www.admin.ksmarter.shop"
# ]


CORS_ALLOW_CREDENTIALS = True


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',
    'corsheaders',
    'graphene_django',
    'authentication',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'common',
    'product',
    'inventory',
    'business',
    'order',
    'settlement',
    'inform',
    'django_admin_listfilter_dropdown',
    'rest_framework',
    'payment',
    'smarter_money',
    'django_extensions',
    'calculate',
    'gym_class',
    'gym_student',
    'class_payment',
    'notification',
    'statistic',
    'scheduler',
    'cs',
]

AUTH_USER_MODEL = 'authentication.User'

GRAPHENE = {
    'SCHEMA': 'server.schema.schema',
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(days=1000),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=1000),
    "JWT_ALLOW_ARGUMENT": True,
}

JWT_COOKIE_SAMESITE = 'Lax'

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]


ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    # 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Asia/Seoul'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CLASS_TOSS_CLIENT_KEY = "test_ck_YZ1aOwX7K8mj2wlNJJm3yQxzvNPG"
# CLASS_TOSS_SECRET_KEY = "test_sk_lpP2YxJ4K87dDJ6nY123RGZwXLOb{}".format(":")
CLASS_TOSS_CLIENT_KEY = "live_ck_5GePWvyJnrKbqOjl21EVgLzN97Eo"
CLASS_TOSS_SECRET_KEY = "live_sk_N5OWRapdA8dY9boemMB3o1zEqZKL{}".format(":")
TOSS_CLIENT_KEY = "live_ck_5GePWvyJnrKbqOjl21EVgLzN97Eo"
TOSS_SECRET_KEY = "live_sk_N5OWRapdA8dY9boemMB3o1zEqZKL{}".format(':')
MONEY_TOSS_CLIENT_KEY = 'live_ck_Z0RnYX2w532emdE2mJe8NeyqApQE'
MONEY_TOSS_SECRET_KEY = 'live_sk_oeqRGgYO1r5KxaqPRBO3QnN2Eyaz{}'.format(':')

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")


CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_ENABLE_UTC = False


LOG_FILE = os.path.join(os.path.dirname(__file__), '../logs', 'myLog.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'myFormatt': {
            'format': '[%(asctime)s] %(levelname)s %(message)s', 'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FILE,  # 위에 선언한 파일 이름
            'when': "midnight",  # 매 자정마다
            'formatter': 'myFormatt',
            'backupCount': 5,
        },
    },
    'loggers': {
        'myLog': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
logger = logging.getLogger('myLog')
