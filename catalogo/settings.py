import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-#18in1x0d5$a#cy8bla5std-uw13fbx+l@23y!ouyw9&f!th5@')

DEBUG = config('DJANGO_DEBUG', default='True') != 'False'

ALLOWED_HOSTS = config(
    'DJANGO_ALLOWED_HOSTS',
    default='localhost,127.0.0.1,.elasticbeanstalk.com',
    cast=Csv()
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "storages",
    "produtos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "catalogo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "catalogo.wsgi.application"

# --- Banco de Dados ---
# Usa MySQL quando DB_HOST estiver definido (produção/RDS), caso contrário SQLite (desenvolvimento local)
_db_host = config('DB_HOST', default='')

if _db_host:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME', default='ap2db'),
            'USER': config('DB_USER', default='admin'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': _db_host,
            'PORT': config('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --- Armazenamento de Mídia ---
# Usa S3 quando AWS_STORAGE_BUCKET_NAME estiver definido, caso contrário armazena localmente
_aws_bucket = config('AWS_STORAGE_BUCKET_NAME', default='')

if _aws_bucket:
    # Credenciais opcionais: se não definidas, boto3 usa o EC2 Instance Role automaticamente
    _aws_key = config('AWS_ACCESS_KEY_ID', default='')
    _aws_secret = config('AWS_SECRET_ACCESS_KEY', default='')
    if _aws_key:
        AWS_ACCESS_KEY_ID = _aws_key
    if _aws_secret:
        AWS_SECRET_ACCESS_KEY = _aws_secret

    AWS_STORAGE_BUCKET_NAME = _aws_bucket
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }

    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# --- Arquivos estáticos ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# --- Validação de senhas ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internacionalização ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
