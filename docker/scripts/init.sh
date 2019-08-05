#!/bin/bash

# call the python script that uses pyscopg2 to check for database connections
# NOTE: we pass in "db" as a parameter since this is the hostname Docker sets for us (in the docker-compose.yml)

bash docker/scripts/wait_for_postgres.sh

bash docker/scripts/generate_secret_key.sh

# Run migrations.
python manage.py migrate

# Create the admin user.
python manage.py init_admin_user
# python docker/scripts/create_admin.py

# Collect static for non-development.
if [ "$DJANGO_ENVIRONMENT" != "development" ]
then
python manage.py collectstatic --no-input
fi

# manage.py for development, otherwise, gunicorn
if [ "$DJANGO_ENVIRONMENT" = "development" ]
then
python manage.py runserver 0.0.0.0:8000
else
# gunicorn wsgi:application --bind 0.0.0.0:8000
gunicorn dcc.wsgi:application --bind 0.0.0.0:8000
fi

# # Execute anything in the "CMD" definition
# exec "$@"
