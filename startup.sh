#!/bin/bash
echo "=== STARTUP SCRIPT BEGINNING ==="
python manage.py collectstatic --noinput
python manage.py migrate
echo "=== STARTUP SCRIPT COMPLETED, RUNNING SERVER ==="
gunicorn --bind=0.0.0.0:8000  \
    --timeout 600 \
    --access-logfile=- \
    --error-logfile=- \
    --log-level=info \
    myproject.wsgi:application