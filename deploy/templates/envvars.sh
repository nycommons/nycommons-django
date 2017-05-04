#
# Required environment variables for nycommons-django
#
# Copy this file, update the necessary variables, and source the file when
# developing. You might want to automatically source it after your virtualenv
# for the project is activated.
#
# All of these variables should be present, those marked *optional* can be left
# blank.
#

# Database (required)
export NYCOMMONS_DB_NAME='nycommons'
export NYCOMMONS_DB_USER='nycommons'
export NYCOMMONS_DB_PASSWORD=''
export NYCOMMONS_DB_HOST='localhost'
export NYCOMMONS_DB_PORT=''

# Secret key for Django (required, but you can leave it as is)
export NYCOMMONS_SECRET_KEY='secret'

# Base URL where the site is served in development
export NYCOMMONS_BASE_URL='http://localhost:8000'

# Recaptcha (optional)
export NYCOMMONS_RECAPTCHA_PRIVATE_KEY=''
export NYCOMMONS_RECAPTCHA_PUBLIC_KEY=''

# Participant salt for generating IDs (optional)
export NYCOMMONS_ORGANIZE_PARTICIPANT_SALT=''

# Default PK for actors with activity stream (optional)
export NYCOMMONS_ACTSTREAM_DEFAULT_ACTOR_PK=1

# Mailreader (optional, only used in production)
export NYCOMMONS_MAILREADER_HOST=''
export NYCOMMONS_MAILREADER_HOST_USER=''
export NYCOMMONS_MAILREADER_HOST_PASSWORD=''

# Mailchimp (optional, only used in production)
export NYCOMMONS_MAILCHIMP_API_KEY=''
export NYCOMMONS_MAILCHIMP_LIST_ID=''

# Memcache (optional)
export NYCOMMONS_MEMCACHE_LOCATION=''

# Living Lots NYC API key (optional)
export NYCOMMONS_LLNYC_API_KEY=''
