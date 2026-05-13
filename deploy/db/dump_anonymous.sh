#!/bin/bash

export PGPASSWORD=$NYCHAREALTALK_DB_PASSWORD
psql -U $NYCHAREALTALK_DB_USER -d $NYCHAREALTALK_DB_NAME < deploy/db/anonymize.sql

pg_dump --no-owner $NYCHAREALTALK_DB_NAME | gzip > nycharealtalk.sql.gz
