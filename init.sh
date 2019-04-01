#!/bin/bash

# call the python script that uses pyscopg2 to check for database connections
# NOTE: we pass in "db" as a parameter since this is the hostname Docker sets for us (in the docker-compose.yml)

bash wait_for_postgres.sh

bash generate_secret_key.sh

# Create the admin user.
python create_admin.py

# Execute anything in the "CMD" definition
exec "$@"