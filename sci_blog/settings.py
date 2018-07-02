import os
import raven
from configurations import Configuration, values


class BaseConfig(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = 'v)=y&*d5z$5*i9m-vsw_64s$o*)ith^r4ys6nnt&as1+j#f8se'

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'users_app',
        'raven.contrib.django.raven_compat',
    ]

    MIDDLEWARE = [
        'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'sci_blog.urls'

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

    WSGI_APPLICATION = 'sci_blog.wsgi.application'

    DATABASES = values.DatabaseURLValue(environ_name='DB_URI')

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

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    RAVEN_CONFIG = {
        'dsn': values.Value(environ_name='RAVEN_DSN'),
    }


class Dev(BaseConfig):
    DEBUG = True


class Prod(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY_DJANGO')


class Test(BaseConfig):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('PROJECT_NAME'),
            'USER': os.getenv('PROJECT_NAME'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
