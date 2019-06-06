#!/bin/bash

# call the python script that uses pyscopg2 to check for database connections
# NOTE: we pass in "db" as a parameter since this is the hostname Docker sets for us (in the docker-compose.yml)

python docker/scripts/wait_for_postgres.py $POSTGRES_DB

