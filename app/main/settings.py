"""
Django settings for ldmpweb project.
"""

from pathlib import Path
import os
import ast


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

FORCE_SCRIPT_NAME = os.getenv('FORCE_SCRIPT_NAME', '')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!sxg#_zjx^3jcg*0twy^@(04^()_mu59lj4&^s1zr4a+6-io19'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'job',
    'core',
    'crispy_forms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'template_filters': 'main.template_filters',
            }
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get("POSTGRES_DB", 'ldmpdb'),
        'USER': os.environ.get("POSTGRES_USER", 'postgres'),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", 'postgres'),
        'HOST': os.environ.get("POSTGRES_HOST", 'localhost'),
        'PORT': os.environ.get("POSTGRES_PORT", 5435),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


DATE_FORMAT = "Y-m-d"


STATIC_ROOT = os.getenv('STATIC_ROOT',
                        os.path.join(BASE_DIR, "static_root")
                        )

STATIC_URL = os.getenv('STATIC_URL', '%s/static/' % FORCE_SCRIPT_NAME)

_DEFAULT_STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATICFILES_DIRS = os.getenv('STATICFILES_DIRS', _DEFAULT_STATICFILES_DIRS)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB

# Define email service on GeoNode
EMAIL_ENABLE = ast.literal_eval(os.getenv('EMAIL_ENABLE', 'False'))

if EMAIL_ENABLE:
    EMAIL_BACKEND = os.getenv(
        'DJANGO_EMAIL_BACKEND',
        default='django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', 'localhost')
    EMAIL_PORT = os.getenv('DJANGO_EMAIL_PORT', 25)
    EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_TLS = ast.literal_eval(
        os.getenv('DJANGO_EMAIL_USE_TLS', 'False'))
    DEFAULT_FROM_EMAIL = os.getenv(
        'DEFAULT_FROM_EMAIL', 'Trends.Earth <no-reply@trends.earth.org>')
else:

    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/home/app/emails'


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Security stuff
SESSION_EXPIRED_CONTROL_ENABLED = ast.literal_eval(
    os.environ.get('SESSION_EXPIRED_CONTROL_ENABLED', 'True'))


SESSION_COOKIE_SECURE = ast.literal_eval(
    os.environ.get('SESSION_COOKIE_SECURE', 'False'))
CSRF_COOKIE_SECURE = ast.literal_eval(
    os.environ.get('CSRF_COOKIE_SECURE', 'False'))
CSRF_COOKIE_HTTPONLY = ast.literal_eval(
    os.environ.get('CSRF_COOKIE_HTTPONLY', 'False'))
CORS_ORIGIN_ALLOW_ALL = ast.literal_eval(
    os.environ.get('CORS_ORIGIN_ALLOW_ALL', 'False'))
X_FRAME_OPTIONS = os.environ.get('X_FRAME_OPTIONS', 'SAMEORIGIN')
SECURE_CONTENT_TYPE_NOSNIFF = ast.literal_eval(
    os.environ.get('SECURE_CONTENT_TYPE_NOSNIFF', 'True'))
SECURE_BROWSER_XSS_FILTER = ast.literal_eval(
    os.environ.get('SECURE_BROWSER_XSS_FILTER', 'True'))
SECURE_SSL_REDIRECT = ast.literal_eval(
    os.environ.get('SECURE_SSL_REDIRECT', 'False'))
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '3600'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = ast.literal_eval(
    os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True'))


SITE_HOST_SCHEMA = os.getenv('SITE_HOST_SCHEMA', 'http')
SITE_HOST_NAME = os.getenv('SITE_HOST_NAME', 'localhost')
SITE_HOST_PORT = os.getenv('SITE_HOST_PORT', 80)
_default_siteurl = "%s://%s:%s/" % (
    SITE_HOST_SCHEMA,
    SITE_HOST_NAME,
    SITE_HOST_PORT) if SITE_HOST_PORT else "%s://%s/" % (
        SITE_HOST_SCHEMA, SITE_HOST_NAME)
SITEURL = os.getenv('SITEURL', _default_siteurl)
SITENAME = os.getenv('SITENAME', "Trends.Earth")


# API Settings
API_URL = 'https://api.trends.earth'
TIMEOUT = 200