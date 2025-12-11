#!/bin/sh
set -e

#Gunicorn palaišanas scripts
: "${DB_HOST:=127.0.0.1}"
: "${DB_PORT:=3306}"
: "${GUNICORN_WORKERS:=3}"

echo "Waiting for database ${DB_HOST}:${DB_PORT}..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

python manage.py migrate --noinput
python manage.py collectstatic --noinput


exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers "$GUNICORN_WORKERS"
