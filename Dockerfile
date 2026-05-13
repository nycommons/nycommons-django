FROM python:2.7-slim

# python:2.7-slim is Debian Buster (EOL June 2024); repos moved to archive
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/10archive \
    && printf 'deb http://archive.debian.org/debian buster main\ndeb http://archive.debian.org/debian-security buster/updates main\n' \
       > /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    g++ \
    gcc \
    gdal-bin \
    git \
    libgdal-dev \
    libgeos-dev \
    libjpeg-dev \
    libpq-dev \
    libproj-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/ requirements/
# Install Django first — some packages (django-monitor) import it in setup.py.
# Build psycopg2 from source to avoid manylinux wheel glibc symbol conflicts.
RUN pip install --no-cache-dir Django==1.11.8 \
    && pip install --no-cache-dir --no-binary psycopg2 psycopg2==2.7.1 \
    && pip install --no-cache-dir \
    -r requirements/base.txt \
    -r requirements/local.txt
# django-appconf 0.6.0 references django.utils.importlib which was removed in
# Django 1.9; Python 2.7 has a standard-library importlib so the fix is safe.
RUN sed -i 's/from django.utils.importlib import import_module/from importlib import import_module/' \
    /usr/local/lib/python2.7/site-packages/appconf/utils.py

COPY . .

WORKDIR /app/nycommons

ENV DJANGO_SETTINGS_MODULE=nycommons.settings.local

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
