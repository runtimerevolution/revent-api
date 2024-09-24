import os
from pathlib import Path

from environ import Env

__env = Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Raises Django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = __env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = __env.bool("DEBUG", default=False)

# AWS environment variables
AWS_S3_ENDPOINT_URL = __env.url("AWS_S3_ENDPOINT_URL").geturl()
AWS_DEFAULT_REGION = __env.str("AWS_DEFAULT_REGION")
AWS_STORAGE_BUCKET_NAME = __env.str("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = __env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = __env.str("AWS_SECRET_ACCESS_KEY")
AWS_QUERYSTRING_AUTH = __env.bool("AWS_QUERYSTRING_AUTH")
AWS_S3_SIGNATURE_VERSION = __env.str("AWS_S3_SIGNATURE_VERSION")  # "s3v4"

print(AWS_S3_ENDPOINT_URL)

# Other environment variables
MAX_PICTURE_SIZE = __env.int("MAX_PICTURE_SIZE", default=80000000)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "strawberry.django",
    "corsheaders",
    "photo",
    "storages",
    "rest_framework",
    "django_extensions",
    "rest_framework.authtoken",
    "djoser",
    "social_django",
]

MIDDLEWARE = [
    "whitenoise.runserver_nostatic",
    "utils.middleware.HealthCheckMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ALLOWED_HOSTS = __env.list("ALLOWED_HOSTS", default=[])
CORS_ALLOWED_ORIGINS = __env.list("CSRF_TRUSTED_ORIGINS", default=[])
CORS_ORIGIN_WHITELIST = __env.list("CORS_ORIGIN_WHITELIST", default=[])
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = __env.list("CSRF_TRUSTED_ORIGINS", default=[])

DJOSER = {
    "LOGIN_FIELD": "email",
    "SOCIAL_AUTH_TOKEN_STRATEGY": "config.strategy.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": __env.list("ALLOWED_REDIRECT_URIS", default=[]),
}

REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.TokenAuthentication",)}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = __env.str("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = __env.str("GOOGLE_CLIENT_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ["first_name", "last_name"]
SESSION_COOKIE_SAMESITE = None

ROOT_URLCONF = "config.urls"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "photo.User"
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": __env.str("POSTGRES_DB"),
        "USER": __env.str("POSTGRES_USER"),
        "PASSWORD": __env.str("POSTGRES_PASSWORD"),
        "HOST": __env.str("POSTGRES_HOST"),
        "PORT": __env.int("POSTGRES_PORT", default=5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "staticfiles/"
STATIC_ROOT = "/efs/staticfiles/"
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django-storages

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "location": AWS_S3_ENDPOINT_URL,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
BASE_BACKEND_URL = __env.url("BASE_BACKEND_URL").geturl()
BASE_APP_URL = __env.url("BASE_APP_URL").geturl()
