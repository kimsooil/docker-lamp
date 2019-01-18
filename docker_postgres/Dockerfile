FROM postgres:9.6

# Use the below script to initialize a user, set their password, and create a blank database
#   NOTE: Must set environment variables to create new user/database (apart from the postgres user):
#   - DATABASE_USER
#   - DATABASE_PASSWORD
#   - DATABASE_NAME
#
#   (hint: can set with `-e 'DATABASE_USER=username'` flags in the `docker run` command)
COPY setup_database.sh /docker-entrypoint-initdb.d/setup_database.sh
RUN chmod +x /docker-entrypoint-initdb.d/setup_database.sh

# Expose port 5432 so we can connect to it from outside the container
EXPOSE 5432

# Be sure to switch to the "postgres" user so we can run the above script and start the service
USER postgres