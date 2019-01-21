#!/bin/bash

# call the python script that uses pyscopg2 to check for database connections
# NOTE: we pass in "db" as a parameter since this is the hostname Docker sets for us (in the docker-compose.yml)
printenv

python wait_for_postgres.py db

# Execute anything in the "CMD" definition
exec "$@"