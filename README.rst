NYCommons
=========

NYCommons.org helps New Yorkers impact decisions about public land and buildings in their neighborhoods. It is a collaboration between Common Cause/NY, the Community Development Project at the Urban Justice Center, and 596 Acres, Inc.

This site uses the `Living Lots <https://github.com/596acres/django-livinglots>`_ ® framework by `596 Acres <https://596acres.org>`_ ®.


Installation
------------

Prerequisites
*************

 1. Python 2.x.
 2. `Postgres <https://www.postgresql.org/>`_ and `PostGIS <http://postgis.net/>`_. Depending on your OS this can be relatively painless.
    * Add a user and database specifically for NYCommons with PostGIS enabled on it. It may be easiest to keep both named `nycommons`.
    * Load a development database snapshot.
 3. node LTS version 6.10.* and npm.

Install the NYCommons Django project
************************************

 1. Clone this repo locally.
 2. Create a Python environment where your requirements will be saved with `virtualenv <https://virtualenv.pypa.io/en/stable/>`_ and `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_.
 3. Install the requirements: `pip install -r requirements/base.txt` and `pip install -r requirements/local.txt`.
 4. Set all the required environment variables in your shell. Copy [deploy/templates/envvars.sh](https://github.com/nycommons/nycommons-django/blob/master/deploy/templates/envvars.sh) somewhere and source it when developing the project.
 5. With the virtualenv activated, try to run the Django project: `django-admin runserver_plus`. If there are issues with environment variables, the database, or other requirements, they should appear here.
 6. The database dump you loaded will have no useful superusers. Create one with `django-admin createsuperuser`.

Install TileStache
******************

`Tilestache <http://tilestache.org/>`_ serves the points and polygons that appear on the map.

 1. Copy the `tilestache.cfg template <https://github.com/nycommons/nycommons-django/blob/master/deploy/templates/tilestache.cfg/>`_ into a new directory in the project root called `tilestache`. Update the username, database, and password as necessary.
 2. Create the views needed for TileStache to run (`visible_centroids` and `visible_polygons`). You can either run the SQL manually or copy `Makefile.example <https://github.com/nycommons/nycommons-django/blob/master/deploy/Makefile.example>`_ to a file named `Makefile`, set the `DB_NAME` and `DB_USER`, and run `make install_tilestache_views`.
 3. When you run `tilestache-server.py -c tilestache/tilestache.cfg` you should get no errors.

Install the client-side requirements
************************************

 1. `cd nycommons/static`
 2. `npm install`
 3. `grunt dev` should work without any errors.

Putting it all together
***********************

Whenever you're developing for the site you'll want the following processes running:

 1. Django: `django-admin runserver_plus`.
 2. TileStache: `tilestache-server.py -c tilestache/tilestache.cfg`.
 3. Grunt: `cd nycommons/static && grunt dev`.


Organization
------------


License
-------

GNU Affero General Public License. See LICENSE.
