
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-i7_21*+x+72fmlsxmulfa)xi6ptn9axow#=5f3lu%lh39lll6t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'access', 'attend', 'login', 'visualization',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels','corsheaders','django_apscheduler',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
import sys
sys.path.append(r'C:\db_setting')
import jjjdb
DATABASES = jjjdb.DATABASES
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'fms_db',
#         'USER': 'fms_root',
#         'PASSWORD': 'fms_root1!',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS =True


STATIC_URL = "/static/"

STATIC_PATH = os.path.join(
    BASE_DIR, "static"
)  # concatena a pasta static a variavel instanciada base_dir que aponta para a raiz do projeto

STATICFILES_DIRS = (STATIC_PATH,)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




##################################################################################################################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    }
}


# Add CHANNEL_LAYERS
CHANNEL_LAYERS = {
    'default': { 'BACKEND': 'channels_redis.core.RedisChannelLayer',
                'CONFIG': {
                            'hosts': [('127.0.0.1', 6379),],
                            }
                }
    }

#Add STATICFILES_FINDERS 
STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django_plotly_dash.finders.DashAssetFinder',
        'django_plotly_dash.finders.DashComponentFinder'
    ]

#Add PLOTLY_COMPONENTS
PLOTLY_COMPONENTS = [
        'dash_core_components',
        'dash_html_components',
        'dash_renderer',
        'dpd_components']

#Add X_FRAME_OPTIONS = 'SAMEORIGIN' to settings.py to enable frames within HTML documents
X_FRAME_OPTIONS = 'SAMEORIGIN'

#### AP scheduler 설정
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds
SCHEDULER_DEFAULT = True # apps.py 참고

