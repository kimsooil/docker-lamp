# Tests

## Basic folder structure for tests.

app/
    
    tests/
        test_views/
            test_home.py
            test_drf.py

        test_models/
            test_user.py

        test_forms/
            test_registration.py

        test_tools/
            test_registration_email.py
            test_job_submission.py

## Runnig different tests.

Django allows running tests in different levels. During development (or when writing tests), it might not be efficient to run all tests for every small change. Sometimes you just need to test a single item. Django tests allow you to run tests up to the smallest unit of a test, which is a method/function. This will allow you to run tests quickly, then continue development. When you are done, the tests can be done on the next upper level up to the top most level.

### Run ALL tests.

python3 manage.py test

### Run tests in a specific app.

python3 manage.py test app.tests

### Run tests in a specific folder.

python3 manage.py test app.tests.test_views

### Run a specified test class.

python3 manage.py test app.tests.test_views.YourTestClass

### Run a specified method in your test class.

python3 manage.py test app.tests.test_views.YourTestClass.test_a_method_in_this_class

## Running tests on docker.

This project is designed to work with docker. So, in order to run this in a container, do the following.

NOTE: These will be run against the *django* container.

### Docker

*docker exec django_container* python3 manage.py test

### docker-compose

docker-compose run django_container python3 manage.py test

docker-compose -f development-docker-compose.yml run python3 manage.py test