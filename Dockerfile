FROM python:3
ENV PYTHONUNBUFFERED 1

# Make a location for all of our stuff to go into
RUN mkdir /code

# Set the working directory to this new location
WORKDIR /code

# Copy all of our scripts into the location
ADD requirements/base.txt /code/
ADD requirements/development.txt /code/

# Install requirements for Django
RUN pip install -r base.txt
RUN pip install -r development.txt

# Add our Django code
ADD . /code/

# Expose the port so we can access Django as it's running
EXPOSE 8000

# Set the entry point script
ADD wait_for_postgres.sh /code/
ADD wait_for_postgres.py /code/
RUN chmod +x /code/wait_for_postgres.sh

ENTRYPOINT ["/code/wait_for_postgres.sh"]

# Start the server:
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python3", "manage.py", "runserver", "127.0.0.1:8000"]