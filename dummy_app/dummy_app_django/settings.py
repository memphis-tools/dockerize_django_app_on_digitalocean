from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# used to get the SECRET_KEY and the SQL_PASSWORD (source: https://en.ovcharov.me/2021/09/30/use-docker-secrets-in-django/)
def get_secret(key, default):
    value = os.getenv(key, default)
    if os.path.isfile(value):
        with open(value) as f:
            return f.read().strip()
    return value

SECRET_KEY = get_secret("SECRET_KEY", "")
DEBUG = int(os.getenv("DEBUG", default=0))
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = [f"http://{ALLOWED_HOSTS[0]}:5555"]

# Add to project/settings.py
SECURE_HSTS_SECONDS = 2_592_000  # 30 days

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'litreview',
    'django_bootstrap_icons',
    'bootstrap5',
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

ROOT_URLCONF = 'dummy_app_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath("templates")],
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

WSGI_APPLICATION = 'dummy_app_django.wsgi.application'

DATABASES = {
    "default": {
        'ENGINE': os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": get_secret("SQL_PASSWORD", ""),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": int(os.environ.get("SQL_PORT")),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.joinpath("static")]
STATIC_ROOT = BASE_DIR / "staticfiles"
AUTH_USER_MODEL = 'authentication.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'feed'
LOGOUT_REDIRECT_URL = LOGIN_URL
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "mediafiles"

# Custom
MAX_ITEMS_PER_PAGE = 5
IMAGE_PREFERED_SIZE = (300, 425)
