# Generating a secret key.

## How to.

The *SECRET_KEY* is generated and stored in a file using the 'django-generate-secret-key' module. The command is as follows:

### Without docker
```bash
python3 manage.py generate_secret_key --replace
```

### Using docker:

```bash
docker exec container_name python3 manage.py generate_secret_key --replace
```

The command stores the key in a file called *secretkey.txt*. The key is then read into the *settings.py* file on runtime. 

**NOTE**: To replace the key, use the *--replace* flag.