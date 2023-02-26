import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY', '40r-my-5&cr&+k#y')
DEBUG = True if os.getenv('DEBUG') == 'YES' else False
ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS", "*")]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'mailing.apps.MailingConfig',
    'bootstrap_modal_forms',
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

ROOT_URLCONF = 'send_mail.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'send_mail.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.getenv("ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("POSTGRES_DB", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.getenv("POSTGRES_USER", "user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_SERVER", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }, }


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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

if os.getenv("EMAIL_FILE_BACKEND") == "YES":
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True if os.getenv("EMAIL_USE_TLS") == "YES" else False
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")


REDIS_SERVER = os.getenv("REDIS_SERVER", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)

CELERY_BROKER_URL = ("redis://" + REDIS_SERVER + ":" + REDIS_PORT + "/"
                     + REDIS_DB)
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
