# Generating a secret key.

## How to.

The *SECRET_KEY* is automatically generated when container is first initialized. If a 'secretkey.txt' file does not exist, one is created with a new *SECRET_KEY* value.

### Replacing the *SECRET_KEY*

Replacing the *SECRET_KEY* requires a django restart. In order to do this (i.e. replace the key), delete the *secretkey.txt* file and run 

```bash
docker-compose up --rebuild
```