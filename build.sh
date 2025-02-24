#!/bin/bash
set -e

echo "making the  migrations..."
python manage.py makemigrations 

echo "Running migrations..."
python manage.py migrate --noinput

echo "Populating sample data..."
python manage.py populate_samples

echo "Creating superuser from environment variables..."
python manage.py create_superuser_from_env

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete."
