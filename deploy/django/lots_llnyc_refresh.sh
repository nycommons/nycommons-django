#!/bin/bash

source $HOME/.bashrc
workon $NYCOMMONS_VIRTUAL_ENV
django-admin lots_llnyc_refresh
