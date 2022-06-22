"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os.path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # api
SRC_DIR = BASE_DIR.parent

# environment file
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=os.path.join(SRC_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# ALLOWED_HOSTS = ["[::1]", "127.0.0.1", "localhost"]
ALLOWED_HOSTS = ["*"]

# Application definition
MBTMI_APPS = [
    "posts",
    "comments",
    "reactions",
    "reports",
    "surveys",
    "users"
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # django-rest-framework
    "rest_framework",
    "rest_framework.authtoken",
    # api documentation
    "drf_spectacular",
    # jwt: json web token
    "rest_framework_simplejwt.token_blacklist",
    # dj-rest-auth
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # django-allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    # cors
    "corsheaders",
    # useful extentions
    "django_extensions",
    # for debugging
    "debug_toolbar",
] + MBTMI_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug toolbar
    'django.middleware.common.CommonMiddleware',
    "config.middleware.csrf.DisableCSRF",  # csrf disable (temporary)
    # "django.middleware.csrf.CsrfViewMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# user model
# AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")  # caution

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")  # caution

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Time stamp format
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"


# drf settings
REST_FRAMEWORK = {
    # camel case converter
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
    ),
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
    # API document automation: drf-spectacular
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Permit only to authenticated user
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    # time stamp format
    "DATETIME_FORMAT": DATETIME_FORMAT,
    "DATE_FORMAT": DATE_FORMAT,
    "TIME_FORMAT": TIME_FORMAT,
}

# oauth
KAKAO_REST_API_KEY = env("OAUTH_KAKAO_CLIENT_ID")
KAKAO_SECRET = env("OAUTH_NAVER_SECRET")
KAKAO_REDIRECT_URL = '/users/login/callback'

SOCIALACCOUNT_ADAPTER = "users.adapter.UserAdapter"
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env("OAUTH_GOOGLE_CLIENT_ID"),
            "secret": env("OAUTH_GOOGLE_SECRET"),
            "key": env("OAUTH_GOOGLE_API_KEY"),
        },
        "SCOPE": [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/user.birthday.read",
            "https://www.googleapis.com/auth/user.phonenumbers.read",
        ],
        "UTH_PARAMS": {
            "access_type": "online",
        },
    },
    "kakao": {
        "APP": {
            "client_id": KAKAO_REST_API_KEY,
            'redirect_uri': KAKAO_REDIRECT_URL,
            'response_type': 'code',
            "secret": KAKAO_SECRET,
        },
        "SCOPE": ["profile_nickname", "account_email"],
    },
}


# jwt
REST_USE_JWT = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=72),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=144),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}
USER_ID_FIELD = "username"

REST_AUTH_SERIALIZERS = {
    "LOGIN_SERIALIZER": "users.serializers.UserLoginSerializer",
    "REGISTER_SERIALIZER": "users.serializers.UserSignUpSerializer",
    "USER_DETAILS_SERIALIZER": "users.serializers.OAuthLoginUserSerializer",
}

AUTHENTICATION_BACKENDS = {
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
}


SPECTACULAR_SETTINGS = {
    "TITLE": "엠비티엠아이 API",
    "DESCRIPTION": "SW중심대학 해커톤 2022",
    "CONTACT": {
        "name": "팀 뫄뫄",
        "url": "https://github.com/sw-hackathon-2022/mbtmi-backend",
        "email": "sw.hcak.2022@gmail.com",
    },
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SERVE_AUTHENTICATION": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "CAMELIZE_NAMES": True,
    "ENABLE_DJANGO_DEPLOY_CHECK": True,
    # TODO
    "SERVERS": [
        {"url": "http://localhost/", "description": "Local server"},
        {"url": "https://development.server.link.todo/", "description": "Development server"},
    ],
    "SWAGGER_UI_SETTINGS": {
        "dom_id": "#swagger-ui",  # required(default)
        "layout": "BaseLayout",  # required(default)
    },
    "DISABLE_ERRORS_AND_WARNINGS": True,
}
