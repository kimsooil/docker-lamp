# Stuff


## Basic interaction with the containers.

### General contain

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
