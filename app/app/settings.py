from pathlib import Path
from os import environ
import random
from string import punctuation, digits, ascii_letters

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY', repr(''.join([
    random.SystemRandom().choice(
        ascii_letters + digits + punctuation
    ) for i in range(random.randint(45, 50))])
))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(environ.get('DEBUG', '0')))

ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', '127.0.0.1 0.0.0.0').split(' ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'checker.apps.CheckerConfig',
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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': environ.get('SQL_DATABASE', str(BASE_DIR / "db.sqlite3")),
        'USER': environ.get('SQL_USER', 'user'),
        'PASSWORD': environ.get('SQL_PASSWORD', 'password'),
        'HOST': environ.get('SQL_HOST', 'localhost'),
        'PORT': environ.get('SQL_PORT', '5432')
    }
}

if environ.get('SQL_ENGINE') == 'django.db.backends.mysql':
    DATABASES['default']['OPTIONS'] = dict()
    DATABASES['default']['OPTIONS']['init_command'] = "SET sql_mode='STRICT_TRANS_TABLES'"

    # Fake PyMySQL's version and install as MySQLdb
    # https://adamj.eu/tech/2020/02/04/how-to-use-pymysql-with-django/
    import pymysql
    pymysql.version_info = (1, 4, 2, "final", 0)
    pymysql.install_as_MySQLdb()


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# LDAP
if environ.get('LDAP_URI', False):
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfUniqueNamesType

    AUTH_LDAP_SERVER_URI = environ['LDAP_URI']
    AUTH_LDAP_BIND_DN = environ['LDAP_BIND_DN']
    AUTH_LDAP_BIND_PASSWORD = environ['LDAP_BIND_PASS']
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        environ['LDAP_USERS'],
        ldap.SCOPE_SUBTREE,
        '(uid=%(user)s)',
    )
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        environ['LDAP_GROUPS'],
        ldap.SCOPE_SUBTREE,
        '(objectClass=groupOfUniqueNames)',
    )
    AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType(name_attr='cn')

    AUTH_LDAP_REQUIRE_GROUP = environ['LDAP_GROUP']

    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        'is_active': environ['LDAP_GROUP'],
        'is_staff': environ['LDAP_SUPERGROUP'],
        'is_superuser': environ['LDAP_SUPERGROUP'],
    }

    AUTH_LDAP_GROUP_CACHE_TIMEOUT = 0
    AUTH_LDAP_CACHE_GROUPS = 0
    AUTH_LDAP_ALWAYS_UPDATE_USER = True
    AUTH_LDAP_FIND_GROUP_PERMS = True
    AUTH_LDAP_CACHE_TIMEOUT = 0

    AUTHENTICATION_BACKENDS += ['django_auth_ldap.backend.LDAPBackend']

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"console": {"class": "logging.StreamHandler"}},
        "loggers": {"django_auth_ldap": {"level": "INFO", "handlers": ["console"]}},
    }

# OAuth
if environ.get('OAUTH_URL', False):
    INSTALLED_APPS += 'oauth2_provider'
    AUTHENTICATION_BACKENDS += 'oauth2_provider.backends.OAuth2Backend'
    MIDDLEWARE += 'oauth2_provider.middleware.OAuth2TokenMiddleware'

    OAUTH_URL = environ.get('OAUTH_URL')
    OAUTH_CLIENT_ID = environ.get("OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET = environ.get('OAUTH_CLIENT_SECRET')
    AUTHENTICATION_BACKENDS += ['oauth2_provider.backends.OAuth2Backend']

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
