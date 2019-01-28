FROM python:3
ENV PYTHONUNBUFFERED 1

# Make a location for all of our stuff to go into
RUN mkdir /app

# Set the working directory to this new location
WORKDIR /app

# Add our Django code
ADD . /app/

# # Copy all of our scripts into the location
# ADD requirements/base.txt /code/
# ADD requirements/development.txt /code/

# Install requirements for Django
RUN pip install -r requirements/base.txt
RUN pip install -r requirements/development.txt

# Expose the port so we can access Django as it's running
EXPOSE 8000

# # Set the entry point script
# ADD wait_for_postgres.sh /code/
# ADD wait_for_postgres.py /code/
RUN chmod +x /app/init.sh
RUN chmod +x /app/wait_for_postgres.sh
RUN chmod +x /app/generate_secret_key.sh

ENTRYPOINT ["/app/init.sh"]

# Start the server:
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["python3", "manage.py", "runserver", "127.0.0.1:8000"]