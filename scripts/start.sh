#!/bin/bash

nohup python celery_main.py > celery.log 2>&1 &

venv/bin/gunicorn analysis-api.wsgi:application -b 0.0.0.0:8976
