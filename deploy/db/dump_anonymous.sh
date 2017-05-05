#!/bin/bash

export PGPASSWORD=$NYCOMMONS_DB_PASSWORD
psql -U $NYCOMMONS_DB_USER -d $NYCOMMONS_DB_NAME < deploy/db/anonymize.sql

pg_dump --no-owner $NYCOMMONS_DB_NAME | gzip > nycommons.sql.gz
