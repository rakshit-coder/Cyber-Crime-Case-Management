"""
Django settings for secure_case_connect project.
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'users',
    'complaints',
    'cases',
    'laws',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'secure_case_connect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'secure_case_connect.wsgi.application'

# Database - SQLite for Development (can switch to MySQL in production)
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': os.path.join(BASE_DIR, config('DB_NAME', default='db.sqlite3')),
    }
}

# For production with MySQL, uncomment below and update .env:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config('DB_NAME', default='secure_case_connect'),
#         'USER': config('DB_USER', default='root'),
#         'PASSWORD': config('DB_PASSWORD', default='password'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='3306'),
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         }
#     }
# }

# Password validation (CERT-IN compliant)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'utils.validators.CERTINPasswordValidator',  # CERT-IN: 16-21 chars with uppercase, lowercase, digits, special chars
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Multi-language Support
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('hi', _('Hindi - हिंदी')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Language Cookie Settings (for persisting language preference)
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 31536000  # 1 year in seconds
LANGUAGE_COOKIE_SECURE = False  # Set to True in production with HTTPS
LANGUAGE_COOKIE_HTTPONLY = False  # Allow JavaScript access
LANGUAGE_COOKIE_SAMESITE = 'Lax'

# Session Settings (for language in sessions)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Static and Media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# CORS Configuration
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:8000,http://127.0.0.1:8000').split(',')

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Email Configuration (SMTP)
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='noreply@securecaseconnect.com')
BASE_URL = config('BASE_URL', default='http://127.0.0.1:8000')

# Encryption Key (32 bytes for AES-256)
ENCRYPTION_KEY = config('ENCRYPTION_KEY', default='your-32-character-encryption-key-here')

# Security Headers
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'"),
    'style-src': ("'self'", "'unsafe-inline'"),
}
