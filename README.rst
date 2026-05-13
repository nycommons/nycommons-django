nycharealtalk
=========

This is the code behind nycharealtalk.org. It is built upon the
`Living Lots <https://github.com/596acres/django-livinglots>`_ ® framework by `596 Acres <https://596acres.org>`_ ®,
originally developed for nycommons.org.


Development setup
-----------------

Docker (recommended)
********************

Prerequisites: `Docker <https://docs.docker.com/get-docker/>`_ with Compose.

 1. Clone this repo locally.
 2. Copy the environment file and fill in values::

      cp .env.example .env

    The defaults in ``.env.example`` work for local Docker development.
    ``NYCHAREALTALK_SECRET_KEY`` and ``NYCHAREALTALK_ORGANIZE_PARTICIPANT_SALT``
    should be set to non-empty strings.

 3. Start the database and run migrations::

      docker compose up -d db
      docker compose run --rm web python manage.py migrate

    If ``migrate`` fails with a ``column already exists`` error, the database
    has partial state from a previous run. Fake the usercontent migrations and
    retry::

      docker compose run --rm web python manage.py migrate usercontent --fake
      docker compose run --rm web python manage.py migrate

 4. Create the PostGIS views that TileStache reads::

      docker compose exec db psql -U nycharealtalk nycharealtalk \
          -f /docker-entrypoint-initdb.d/create-views.sql

 5. Create a superuser::

      docker compose run --rm web python manage.py createsuperuser

 6. Start all services::

      docker compose up

    The site runs at http://localhost:8000. Map tiles are served at
    http://localhost:8080. The database is accessible from the host on port 5434.

 7. Build the frontend assets (in a separate terminal, from ``nycharealtalk/static/``)::

      npm install
      grunt dev

Loading a database snapshot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To restore a production or staging dump into the Docker database::

    docker compose exec -T db psql -U nycharealtalk nycharealtalk < dump.sql

After restoring, re-run the TileStache views step above since they may not be
included in the dump.

Manual setup (legacy)
*********************

Prerequisites:

 1. Python 2.x with virtualenv/virtualenvwrapper.
 2. `Postgres <https://www.postgresql.org/>`_ and `PostGIS <http://postgis.net/>`_ installed locally. Create a database and user, both named ``nycharealtalk``, with the PostGIS extension enabled.
 3. Node LTS 6.10.x and npm.

 1. Clone this repo locally.
 2. Create and activate a virtualenv, then install requirements::

      pip install -r requirements/base.txt -r requirements/local.txt

 3. Copy ``deploy/templates/envvars.sh`` somewhere, fill in the values, and source it.
 4. Run the Django project::

      python nycharealtalk/manage.py runserver_plus

 5. Copy ``deploy/templates/tilestache.cfg`` to ``tilestache/tilestache.cfg`` and update the database credentials. Create the required views::

      psql -U nycharealtalk nycharealtalk -f docker/create-views.sql

    Then start TileStache::

      tilestache-server.py -c tilestache/tilestache.cfg

 6. Build frontend assets::

      cd nycharealtalk/static && npm install && grunt dev


Organization
------------


License
-------

GNU Affero General Public License. See LICENSE.
