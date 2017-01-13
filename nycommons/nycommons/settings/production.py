import os

from .base import *

ADMINS = (
    ('', 'eric@596acres.org'),
)

# TODO Fill with appropriate managers
MANAGERS = (
    ('', 'manager@example.com'),
)

# TODO Fill with appropriate facilitators
FACILITATORS = {
    'global': [
        'eric@596acres.org',
    ],
}

ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS').split(',')

#
# cache-machine
#

CACHES = {
    'default': {
        'BACKEND': 'caching.backends.memcached.MemcachedCache',
        'LOCATION': [
            get_env_variable('MEMCACHE_LOCATION'),
        ],
    },
}
CACHE_COUNT_TIMEOUT = 60


#
# email
#
INSTALLED_APPS += (
    'mailer',
)
EMAIL_BACKEND = 'mailer.backend.DbBackend'
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = get_env_variable('SERVER_EMAIL')


#
# logging
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'log_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, '../logs', 'django.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['log_file', 'mail_admins'],
        'level': 'WARNING',
    },
}

#
# templates
#
TEMPLATES[0]['OPTIONS']['loaders'] = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'admin_tools.template_loaders.Loader',
    )),
)


#
# SSL
#
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
MAP_SCREENSHOT_URL = "https://nycommons.org/screenshot/"
LOT_TILES_URL = "https://tiles.nycommons.org/lots/{z}/{x}/{y}.json"
PARCELS_URL = "https://tiles.nycommons.org/parcels/{z}/{x}/{y}.json"


#
# Remote lots
#
REMOTE_LOTS = {
    'llnyc': {
        'api_files_url': 'http://livinglotsnyc.org/content/files/export/json/',
        'api_lots_url': 'http://livinglotsnyc.org/lot/geojson/visible/',
        'api_notes_url': 'http://livinglotsnyc.org/content/notes/export/json/',
        'api_organizers_url': 'http://livinglotsnyc.org/organize/export/json/',
        'api_key': get_env_variable('LLNYC_API_KEY'),
        'lot_content_url_pattern': 'https://livinglotsnyc.org/lot/%d/content/json/',
        'lot_permalink_url_pattern': 'http://livinglotsnyc.org/lot/%d/',
        'organizer_permalink_url_pattern': 'http://livinglotsnyc.org/lot/%d/grow-community/organize/%s/edit/',
    },
}
