#!/usr/bin/env bash

export BK_ENV=env

python manage.py collectstatic --no-input && {
    command="gunicorn wsgi -w 10 --timeout 150 -b [::]:5000 -k gevent --max-requests 10240 --access-logfile '-' --access-logformat '%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" in %(L)s seconds' --log-level INFO --log-file=- --env prometheus_multiproc_dir=/tmp/"

    ## Run!
    exec bash -c "$command"
}