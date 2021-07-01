"""
Django settings for eroo project.
"""

import sys
from environs import Env
from pathlib import Path


env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------ Global configuration ------------

ENVIRONMENT = env.str("ENVIRONMENT", default="development")
IS_ENV_DEV = DEBUG = (ENVIRONMENT == "development")
IS_TESTS_IN_PROGRESS = len(sys.argv) > 1 and sys.argv[1] == 'test'

USE_S3 = env.bool("USE_S3", default=False)
USE_MAIL_SERVICE = env.bool("USE_MAIL_SERVICE", default=False)
USE_DEBUG_DATA_STORAGE = env.bool("USE_DEBUG_DATA_STORAGE", default=False)

SITE_ID = 1

# ------------ i18n ------------

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ------------ scrapper configurations ------------

SCRAPPER_USE_FAKE_FILES = env.bool("SCRAPPER_USE_FAKE_FILES", default=False)
AIRBNB_API_KEY = env.str("AIRBNB_API_KEY")

# ------------ logging/exception handling configurations ------------

if not IS_ENV_DEV:
    SENTRY_DSN = env.str("SENTRY_DSN")
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

if not IS_TESTS_IN_PROGRESS:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                        'pathname=%(pathname)s lineno=%(lineno)s ' +
                        'funcname=%(funcName)s %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'scrapper': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'websites': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'utils': {
                'handlers': ['console'],
                'level': 'INFO',
            }
        }
    }

# ------------ Keys configuration ------------

SECRET_KEY = env.str("SECRET_KEY")
GOOGLE_MAP_API_KEY = env.str("GOOGLE_MAP_API_KEY")

# ------------ Safety configuration ------------

ALLOWED_HOSTS = [".eroo.fr", ".herokuapp.com", "localhost", "127.0.0.1"]

if not IS_ENV_DEV:
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ------------ Account/Allauth configurations ------------

LOGIN_REDIRECT_URL = "dashboard"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
AUTH_USER_MODEL = "accounts.CustomUser"

if not IS_ENV_DEV:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# ------------ Mail configuration ------------

if USE_MAIL_SERVICE:
    EMAIL_HOST = env.str('SMTP_SERVER')
    EMAIL_HOST_USER = env.str('SMTP_LOGIN')
    EMAIL_HOST_PASSWORD = env.str('SMTP_PASSWORD')
    EMAIL_PORT = env.str('SMTP_PORT')
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'contact@eroo.fr'
else:
    # use mailhog
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "127.0.0.1"
    EMAIL_PORT = 1025

# ------------ Celery/Redis configurations ------------

if IS_ENV_DEV:
    BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE
else:
    pass  # TODO: configure heroku redis/celery

# ------------ Application definition ------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "storages",
    # third-party apps
    "allauth",
    "allauth.account",
    # local apps
    "accounts",
    "dashboard",
    "scrapper",
    "websites",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "eroo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR.joinpath("templates")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "eroo.wsgi.application"

# ------------ Database ------------

DATABASES = {"default": env.dj_db_url("DATABASE_URL")}

# ------------ Password validation ------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ------------ Static & Media files ------------

STATIC_LOCATION = 'static'
PUBLIC_MEDIA_LOCATION = 'media'
PRIVATE_MEDIA_LOCATION = 'private'

STATICFILES_DIRS = [str(BASE_DIR / "static")]

if USE_S3:
    # AWS settings
    AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # S3 static settings
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'websites.storage_backends.StaticStorage'

    # S3 public media settings
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'websites.storage_backends.PublicMediaStorage'

    # S3 private media settings
    PRIVATE_FILE_STORAGE = 'websites.storage_backends.PrivateMediaStorage'
else:
    # local static settings
    STATIC_URL = "/static/"
    STATIC_ROOT = str(BASE_DIR / "staticfiles")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # local public media settings
    MEDIA_URL = "/media/"
    MEDIA_ROOT = str(BASE_DIR / "mediafiles")
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    # local private media settings
    PRIVATE_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
