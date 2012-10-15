# Django settings for CONNECT project.

import os
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Chris West', 'chris@fry-it.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1


USE_I18N = True
USE_L10N = False


MEDIA_ROOT = os.path.join(PROJECT_PATH, "static")
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'context_processors.common',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'connect.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates/")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django_static',
    'website',
    'sorl.thumbnail',
    'modeltranslation_wrapper',
    'modeltranslation',
    'tinymce',
)



# django static information
DJANGO_STATIC_SAVE_PREFIX = '/tmp/cache-forever/westlord'
DJANGO_STATIC_NAME_PREFIX = '/cache-forever/westlord'
DJANGO_STATIC = False
DJANGO_STATIC_MEDIA_URL = 'http://static.westlord.co.uk'
MEDIA_URL = '/'


# language stuff
USE_I18N = True
USE_L10N = False
gettext = lambda s: s
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', gettext('English')),
    ('zh', gettext('Chinese')),
)
LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, "locale")
)
MODELTRANSLATION_TRANSLATION_REGISTRY = "translation"
MODELTRANSLATION_AUTO_POPULATE = False


#tinyMCE stuff
TINYMCE_JS_URL = "js/tiny_mce/tiny_mce.js"
TINYMCE_JS_ROOT = "js/tiny_mce"
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace",
    'theme': "advanced",
    'language': 'en',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}

SITE_EMAIL = 'info@connect-china.net'



try:
    from local_settings import *
except ImportError:
    pass

