#!/bin/bash

source $HOME/.bashrc
source $HOME/.virtualenvs/$NYCOMMONS_VIRTUAL_ENV/bin/activate

tilestache-clean.py --config /webapps/nycommons_tilestache/tilestache.cfg --layer ALL --bbox 40.442 -74.483 41.017 -73.521
