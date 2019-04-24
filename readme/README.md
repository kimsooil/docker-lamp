# Getting Started

## README

- Use this readme as the entry point for learning about the project.
- For the most part, each part of the site is mostly documented with READMEs. Please consult these for details about the site.

Keys | Description
----- | -----------
CRC-DCC | CRC Django Cookie Cutter
DCC | Django Cookie Cutter
CC | Cookie Cutter

NOTE: The main 'readme.md' on the root directory is left blank for a reason. It is to be used solely as a starting point for project specific documentation.

Files | Description
----- | -----------
django-oauth-toolkit.md | Description of the toolkit used for authentication purposes and how to use it.
env.md | Describes the envrionment variables used in the CC.
GETTING-STARTED.md | This file. Entry point for CC documentation.
SCRIPTS.md | Describes all the scripts used in the DCC.
secret-key.md | Describes how the secret key used in Django is generated and re-generated.
tests.md | Describes how to setup and run tests.

## Creating a new project.

#### Fork this project

At the moment, forking and renaming is not an option (i.e. only Bitbucket does this). Because of that, go to next instruction.

#### Clone the DCC.

Clone the repository to your desired project name.

```sh
git clone https://github.com/crcresearch/crc-dcc.git project-name-crc-dcc
```

#### New GitHub repo.

Create a new, empty GitHub repo for your new project.

#### Change the 'origin' url.

This step allows you to switch the source of your repository to your new project repository.

```sh
git remote set-url origin https://github.com/crcresearch/project-name-crc-dcc.git
```

#### Push your new repo.

```sh
git push -u origin master
```

#### Upstream.

Add the base git repo as an upstream.

```sh
git remote add upstream https://github.com/crcresearch/crc-dcc.git
```

#### remotes

```sh
git remote -v
```

##### result

```sh
origin	https://github.com/bringthehouse/crc-dcc.git (fetch)
origin	https://github.com/bringthehouse/crc-dcc.git (push)
upstream	https://github.com/crcresearch/crc-dcc.git (fetch)
upstream	https://github.com/crcresearch/crc-dcc.git (push)
```

*NOTE: upstream is the 'base' CRC-DCC repo*

### Updating from upstream.

Let's say that the base CRC-DCC is updated. How do you get the changes to your fork? 


#### Get the updates from upstream.

```sh
git fetch upstream
```

#### Select branch to update.

It is recommended that you update your develop branch (or a test branch) instead of master. We will try to not have breaking changes, but, this will allow you to test your repo in case there are any issues before adding this
```sh
git checkout develop
```

#### Rebase

Running this command will reabase your selected branch with the upstream's (base CRC-DCC) master branch. 

```sh
git rebase upstream/master
```

#### Update your repo.
```sh
git push -f origin develop
```

#### Setup .env file

A *sample.env* file is provided with minimum required environment variables. Copy them to *.env* file and modify it as you wish.

```sh
cat sample.env > .env
```

#### Start your project.

```sh
docker-compose up --build
```

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