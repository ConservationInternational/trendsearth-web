"""
Django settings for ldmpweb project.
"""

from pathlib import Path
import os
import ast


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

FORCE_SCRIPT_NAME = os.getenv('FORCE_SCRIPT_NAME', '')


SECRET_KEY = 'django-insecure-!sxg#_zjx^3jcg*0twy^@(04^()_mu59lj4&^s1zr4a+6-io19'

DEBUG = True

ALLOWED_HOSTS = ['localhost', 'localhost:8000']


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
    'crispy_forms',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000', 'http://trends.earth.s3.us-east-1.amazonaws.com'
)

CORS_ALLOWED_ORIGINS = [
    'http://trends.earth.s3.us-east-1.amazonaws.com',
    'http://localhost:8000'
]

CORS_ALLOW_ALL_ORIGINS = True

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
                'main.context_processors.mailto'
            ],
            'libraries':{
                'template_filters': 'main.template_filters',
            }
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


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


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


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


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB

# Define email service

MAIL_TO_ADMIN = os.getenv('MAIL_TO_ADMIN', 'info@trends.earth')

EMAIL_ENABLE = True

if EMAIL_ENABLE:
    EMAIL_BACKEND = os.getenv(
        'EMAIL_BACKEND',
        default='django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.sparkpostmail.com')
    EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'SMTP_Injection')
    EMAIL_HOST_PASSWORD = os.getenv(
        'EMAIL_HOST_PASSWORD', '1588d5eafd9a0ee1f4acbb4f389c54a4990bf1f6')
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = os.getenv(
        'DEFAULT_FROM_EMAIL', 'info@trends.earth')
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
SITE_HOST_NAME = os.getenv('SITE_HOST_NAME', 'localhost:8000')
SITE_HOST_PORT = os.getenv('SITE_HOST_PORT', 80)
_default_siteurl = "%s://%s:%s/" % (
    SITE_HOST_SCHEMA,
    SITE_HOST_NAME,
    SITE_HOST_PORT) if SITE_HOST_PORT else "%s://%s/" % (
        SITE_HOST_SCHEMA, SITE_HOST_NAME)
SITEURL = os.getenv('SITEURL', _default_siteurl)
SITENAME = os.getenv('SITENAME', "Trends.Earth")


# API Settings
API_URL = os.getenv('API_URL', 'https://api.trends.earth')
TIMEOUT = 200

# Colors
DEGRADED_HEX = '#9b2779'
INCREASING_HEX = '#006500'
STABLE_HEX = '#FFFFE0'
