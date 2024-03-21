from collections import OrderedDict
import os
from os.path import abspath, dirname

from django.core.exceptions import ImproperlyConfigured


ENV_VARIABLE_PREFIX = 'NYCHAREALTALK'

def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    if not ENV_VARIABLE_PREFIX:
        raise ImproperlyConfigured('Set ENV_VARIABLE_PREFIX')
    try:
        return os.environ[ENV_VARIABLE_PREFIX + '_' + var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)


DATABASES = {
    'default': {
        # PostGIS < 2.0:
        #  > createdb -T template_postgis livinglots
        #  > psql
        #  # create user livinglots with password 'password';
        #  # grant all privileges on database livinglots to livinglots;
        #
        # PostGIS >= 2.0:
        #  > createdb livinglots
        #  > psql livinglots
        #  # create extension postgis;
        #  # create extension postgis_topology;
        #  # create user livinglots with password 'password';
        #  # grant all privileges on database livinglots to livinglots;
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
        'CONN_MAX_AGE': 600,
    }
}

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
)

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = 'America/New_York'

PROJECT_ROOT = os.path.join(abspath(dirname(__file__)), '..', '..')

DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = get_env_variable('SECRET_KEY')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'APP_DIRS': True,
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',

                'feincms.context_processors.add_page_if_missing',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
            ]
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'honeypot.middleware.HoneypotMiddleware',
    'reversion.middleware.RevisionMiddleware',
)

ROOT_URLCONF = 'nycommons.urls'

WSGI_APPLICATION = 'nycommons.wsgi.application'

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    # Has to come before django.contrib.admin
    'dal',
    'dal_select2',

    #
    # django contrib
    #
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    #
    # third-party
    #
    'actstream',
    'admin_enhancer',
    'articles',
    'contact_form',
    'django_monitor',
    'djangojs',
    'easy_select2',
    'elephantblog',
    'feincms',
    'feincms.module.medialibrary',
    'feincms.module.page',
    'flatblocks',
    'honeypot',
    'imagekit',
    'inplace',
    'inplace.boundaries',
    'inplace_activity_stream',
    'jsonfield',
    'leaflet',
    'mptt',
    'reversion',
    'svg',
    #'reversion_compare',
    'taggit',
    'tinymce',
    'widget_tweaks',

    #
    # first-party, project-generic
    #
    'pagepermissions',

    #
    # Living Lots
    #
    'livinglots_lots',
    'livinglots_mailings',
    'livinglots_notify',
    'livinglots_organize',
    'livinglots_owners',
    'livinglots_pathways',
    'livinglots_steward',
    'livinglots_usercontent',
    'livinglots_usercontent.files',
    'livinglots_usercontent.notes',
    'livinglots_usercontent.photos',

    #
    # nycdata
    #
    'nycdata',
    'nycdata.citycouncildistricts',
    'nycdata.communitydistricts',
    'nycdata.landmarks',
    'nycdata.libraries',
    'nycdata.nycha',
    'nycdata.parcels',
    'nycdata.parks',
    'nycdata.postoffices',
    'nycdata.shoreline',
    'nycdata.waterfront',
    'nycdata.urbanrenewal',

    #
    # first-party, project-specific
    #
    'activities',
    'blog',
    'cms',
    'congressionaldistricts',
    'contact',
    'faq',
    'foil',
    'groundtruth',
    'lots',
    'organize',
    'organizingpathways',
    'ownerpathways',
    'owners',
    'reviewpathways',
    'steward',
    'usercontent',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

RECAPTCHA_PRIVATE_KEY = get_env_variable('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = get_env_variable('RECAPTCHA_PUBLIC_KEY')

ORGANIZE_PARTICIPANT_SALT = get_env_variable('ORGANIZE_PARTICIPANT_SALT')

ACTSTREAM_SETTINGS = {
    'MANAGER': 'inplace_activity_stream.managers.PlaceActionManager',
}
ACTIVITY_STREAM_DEFAULT_ACTOR_PK = get_env_variable('ACTSTREAM_DEFAULT_ACTOR_PK')

FACILITATORS = {
    'global': [],
}

EMAIL_SUBJECT_PREFIX = '[NYCHA Real Talk] '

MAILREADER_REPLY_PREFIX = 'Reply with text above this line to post a public note.'
MAILREADER_IGNORE_FROM = []
MAILREADER_HOST = get_env_variable('MAILREADER_HOST')
MAILREADER_HOST_USER = get_env_variable('MAILREADER_HOST_USER')
MAILREADER_HOST_PASSWORD = get_env_variable('MAILREADER_HOST_PASSWORD')

TINYMCE_JS_URL = STATIC_URL + 'node_modules/tinymce/tinymce.min.js'
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'node_modules/tinymce')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'link',
    'theme': "modern",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'menubar': False,
    'statusbar': False,
    'toolbar': 'undo redo | bold italic | bullist numlist | link unlink | help',
}

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_richtext.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': TINYMCE_JS_URL,
}

def elephantblog_entry_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('elephantblog_entry_detail', 'elephantblog.urls',
                       kwargs={
                           'year': self.published_on.strftime('%Y'),
                           'month': self.published_on.strftime('%m'),
                           'day': self.published_on.strftime('%d'),
                           'slug': self.slug,
                       })


def elephantblog_categorytranslation_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('elephantblog_category_detail', 'elephantblog.urls',
                       kwargs={ 'slug': self.slug, })


ABSOLUTE_URL_OVERRIDES = {
    'elephantblog.entry': elephantblog_entry_url_app,
    'elephantblog.categorytranslation': elephantblog_categorytranslation_url_app,
}

MIGRATION_MODULES = {
    'articles': 'faq.migrate.article',
    'elephantblog': 'blog.migrate.elephantblog',
    'medialibrary': 'cms.migrate.medialibrary',
    'page': 'cms.migrate.page',
}

HONEYPOT_FIELD_NAME = 'homepage_url'
HONEYPOT_VALUE = 'http://example.com/'

ADMIN_TOOLS_INDEX_DASHBOARD = 'nycommons.admindashboard.LivingLotsDashboard'

LIVING_LOTS = {
    'MODELS': {
        'lot': 'lots.Lot',
        'lotgroup': 'lots.LotGroup',
        'lotlayer': 'lots.LotLayer',
        'organizer': 'organize.Organizer',
        'owner': 'owners.Owner',
        'owner_contact': 'owners.OwnerContact',
        'owner_group': 'owners.OwnerGroup',
        'stewardproject': 'steward.StewardProject',
        'watcher': 'organize.Watcher',
    },
}

REMOTE_LOTS = {
    'llnyc': {
        'api_files_url': 'http://localhost:8002/content/files/export/json/',
        'api_lots_url': 'http://localhost:8002/lot/geojson/visible/',
        'api_notes_url': 'http://localhost:8002/content/notes/export/json/',
        'api_photos_url': 'http://localhost:8002/content/photos/export/json/',
        'api_organizers_url': 'http://localhost:8002/organize/export/json/',
        'api_key': get_env_variable('LLNYC_API_KEY'),
        'lot_content_url_pattern': 'http://localhost:8002/lot/%d/content/json/',
        'lot_permalink_url_pattern': 'http://localhost:8002/lot/%d/',
        'organizer_permalink_url_pattern': 'http://localhost:8002/lot/%d/grow-community/organize/%s/edit/',
    },
}

# TODO replace with project reasons and email addresses
CONTACT_FORM_REASONS = OrderedDict([
    ('The lot I want permission to use is not here.', ['info@example.com',]),
    ('I want to share my land access story.', ['info@example.com',]),
    ('I want to loan or lease my land for a temporary project.', ['info@example.com',]),
    ('I want to invite admins to an event.', ['info@example.com',]),
    ('I want to reach 596 Acres, the team that made this site.', ['paula@596acres.org',]),
    ('I have a press inquiry.', ['info@example.com',]),
])

BLOG_TITLE = 'NYCHA Real Talk Updates'
BLOG_DESCRIPTION = 'Updates from the NYCHA Real Talk project'

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (40.78, -73.92),
    'DEFAULT_ZOOM': 18,
}
