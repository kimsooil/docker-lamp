FROM python:3
ENV PYTHONUNBUFFERED 1

ARG DJANGO_ENVIRONMENT

# Make the static/media folder.
RUN mkdir /var/staticfiles
RUN mkdir /var/mediafiles

# Make a location for all of our stuff to go into
RUN mkdir /app

# Set the working directory to this new location
WORKDIR /app

# Add our Django code
ADD . /app/

RUN pip install --upgrade pip

# Install requirements for Django
RUN pip install -r requirements/base.txt
RUN pip install -r requirements/${DJANGO_ENVIRONMENT}.txt
RUN pip install -r requirements/custom.txt

# Expose the port so we can access Django as it's running
EXPOSE 8000

# Mark scripts as executable.
RUN chmod +x docker/scripts/init.sh
RUN chmod +x docker/scripts/wait_for_postgres.sh
RUN chmod +x docker/scripts/generate_secret_key.sh

ENTRYPOINT ["/app/docker/scripts/init.sh"]

# Start the server:
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["python3", "manage.py", "runserver", "127.0.0.1:8000"]