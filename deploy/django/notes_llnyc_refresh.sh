#!/bin/bash

source $HOME/.bashrc
workon $NYCOMMONS_VIRTUAL_ENV
django-admin notes_llnyc_refresh
