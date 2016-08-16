#!/bin/bash

source $HOME/.bashrc
workon $NYCOMMONS_VIRTUAL_ENV
django-admin send_mail
