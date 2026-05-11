"""
Django settings for taskmanager project.
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-$^3-qmxil8etmshqz2$ocri^3u%ww2%*-dm@*@9z$nmu=+bur@'
)

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if host != '*'
]

if '*' in ALLOWED_HOSTS:
    CSRF_TRUSTED_ORIGINS.append("https://*.railway.app")


# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'projects',
    'tasks',
    'dashboard',

    'rest_framework',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'axes',
]


# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',

    'axes.middleware.AxesMiddleware',
]


ROOT_URLCONF = 'taskmanager.urls'


# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'taskmanager.wsgi.application'


# DATABASE
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# STATIC FILES
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WHITENOISE_MANIFEST_STRICT = False


# CUSTOM USER MODEL
AUTH_USER_MODEL = 'accounts.User'


# LOGIN SETTINGS
LOGIN_URL = 'account_login'

LOGIN_REDIRECT_URL = '/dashboard/'


# AUTHENTICATION BACKENDS
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',

    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
]


# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_TIMEOUT = 10

EMAIL_HOST_USER = config(
    'EMAIL_HOST_USER',
    default='your-email@gmail.com'
)

EMAIL_HOST_PASSWORD = config(
    'EMAIL_HOST_PASSWORD',
    default=''
)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# DJANGO ALLAUTH
SITE_ID = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

ACCOUNT_LOGIN_METHODS = {'email'}

ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# TEMPORARILY DISABLED TO AVOID RAILWAY SMTP ERRORS
ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'


# DJANGO AXES
AXES_FAILURE_LIMIT = 5

AXES_COOLOFF_TIME = 1

AXES_LOCKOUT_TEMPLATE = 'axes/lockout.html'


# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'