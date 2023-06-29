#!/bin/bash

cd /usr/src/app/

source venv/bin/activate

nohup python celery_main.py > celery.log 2>&1 &

venv/bin/gunicorn analysis-api.wsgi -b 0.0.0.0:8976 
