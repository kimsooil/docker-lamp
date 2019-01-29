# Stuff


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


## Getting started

### Applying migrations.

```sh
docker exec container-name python3 manage.py migrate
```

### Create superuser.

Because of the interactive nature of *createsuperuser* django command, the commands needs connection to the container.

#### Connect to the container.
```sh
docker exec -it container-name bash
```

#### Create superuser.

```sh
docker exec container-name python3 manage.py createsuperuser
```

## Flake8 commands.

Running flake8 to check code for things.

```sh
docker exec container-name flake8 app --max-line-length=120 [--exclude] [directory/to/exclude]
```
