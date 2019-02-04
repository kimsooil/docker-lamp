# .env

## Purpose

The *.env* file is used to set and pass in command line arguments to containers. 

## How to.

- Copy the *sample.env* file to *.env*
- Replace all the relevant keys with the appropriate values. **NOTE** The same fields in the *.env* file can also be found in the *ENVIRONMENT* sections in *docker-compose.yml* file. However, in the *docker-compose.yml* file, the keys are 'just' listed (i.e. no values attached). This tells docker to fetch them from current environment which is set using your *.env* file.
- Start your docker file.

## KEYs

Key | Description | Possible/Sample Values
----- | ----- | ----- 
ENVIRONMENT | Set what the 'overall' environment is. | development/production
POSTGRES_DB | Name of the database to create. | django
POSTGRES_USER | The username to use for the database connection. | django
POSTGRES_PASSWORD | The password to use for the database user. | django
DJANGO_SETTINGS_MODULE | Set the main settings file. | dcc.settings