#!/bin/bash
set -e

echo "installing requirements ..."
pip install -r  requirements.txt

echo "making the  migrations..."
python manage.py makemigrations 

echo "Running migrations..."
python manage.py migrate --noinput

# echo "Populating sample data..."
# python manage.py populate_slides

# echo "Populating sample data..."
# python manage.py database_4x4_data_list

echo "Creating superuser from environment variables..."
python manage.py create_superuser_from_env

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete."
