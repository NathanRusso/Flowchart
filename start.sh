#!/bin/sh

gunicorn -c /app/gunicorn.conf.py app:app &

nginx -g "daemon off;"