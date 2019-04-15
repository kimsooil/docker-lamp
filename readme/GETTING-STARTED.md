# Getting Started

## README

- Use this readme as the entry point for learning about the project.
- For the most part, each part of the site is mostly documented with READMEs. Please consult these for details about the site.

Keys | Description
----- | -----------
DCC | Django Cookie Cutter
CC | Cookie Cutter


Files | Description
----- | -----------
django-oauth-toolkit.md | Description of the toolkit used for authentication purposes and how to use it.
env.md | Describes the envrionment variables used in the CC.
GETTING-STARTED.md | This file. Entry point for CC documentation.
SCRIPTS.md | Describes all the scripts used in the DCC.
secret-key.md | Describes how the secret key used in Django is generated and re-generated.
tests.md | Describes how to setup and run tests.

## General development

Because the project uses docker to run, it may be necessary in some cases to have a virtual environment where the IDE can know about installed packages and such. To do this, you can do the following.

NOTE: You can either build this inside the project or outside the project. .gitignore entry has been added for dcc.

```sh
# Create a virtual environment.
virtualenv env-dcc -p python3

# Activate the environment.
source env-dcc/bin/activate

# Install base requirements and developer requirements.
pip install -r requirements/base.txt
pip install -r requirements/development.txt
pip install -r requirements/custom.txt
```

## Basic interaction with the containers.

### General containers

docker exec container-name -it bash

### Connect to a container an use the shell.

docker exec container-name -it bash

### General run a command in a container and exit.

```sh
docker exec container-name [command]
```

#### Example

```sh
docker exec container-name ls
```


## Other

### Applying migrations.

NOTE: Migrations in general are applied when container comes up, however, during development, use this command to run the migrations.

```sh
docker exec container-name python3 manage.py migrate
```

### Create superuser.

NOTE: Creation of the superuser happens during container creation. In the case that you want to create an additional user, use the following directions.

Because of the interactive nature of *createsuperuser* django command, the commands needs connection to the container.

#### Connect to the container.
```sh
docker exec -it container-name bash
```

#### Create superuser.

```python
python3 manage.py createsuperuser
```

## Flake8 commands.

Running flake8 to check code for things.

```sh
docker exec container-name flake8 app --max-line-length=120 [--exclude] [directory/to/exclude]
```

## Wagtail

This is a good summary of how wagtail is being used in the project [https://docs.wagtail.io/en/v2.4/getting_started/integrating_into_django.html]

### Getting Started

Wagtail is already installed. It can be disabled whenever needed.

**NOTE:** Migrations will be run 

## DRF

Since the emphais will be on using DRF + Frontend JS Framework, *django-cors-headers* is needed. cors allows django to add CORS headers to responses. This allows the frontend application (VueJS, ReactJS, Angular, Mobile apps, etc.) to get/post data from the Django application. In the case of development, this is necessarity because, when creating a single page app, the development happens on a separae port, and, as such, the Django application needs to allow Cross-Origin.