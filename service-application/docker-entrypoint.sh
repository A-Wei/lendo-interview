#!/bin/sh
set -e

UVICORN_WORKERS=${UVICORN_WORKERS:-1} # default UVICORN_WORKERS to 1 if not set

exec gunicorn --worker-class uvicorn.workers.UvicornWorker src.main:app \
              --bind 0.0.0.0:8001 \
              --workers=$UVICORN_WORKERS \
              --log-level=debug \
              --worker-tmp-dir /dev/shm \
              --keep-alive 65
