#!/bin/sh
set -e
envsubst < /tilestache/tilestache.cfg.template > /tilestache/tilestache.cfg
exec tilestache-server.py -c /tilestache/tilestache.cfg -p 8080 -i 0.0.0.0
