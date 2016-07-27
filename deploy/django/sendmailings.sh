#!/bin/bash

source $HOME/.bashrc
source $HOME/.virtualenvs/$NYCOMMONS_VIRTUAL_ENV/bin/activate
django-admin sendmailings
