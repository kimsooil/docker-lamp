# Generating a secret key.

## How to.

The *SECRET_KEY* is automatically generated when container is first initialized. If a 'secretkey.txt' file does not exist, one is created with a new *SECRET_KEY* value.

### Replacing the *SECRET_KEY*

Because replacing the *SECRET_KEY* requires a django restart anyway, it is recommended that you simply *delete* the 'secretkey.txt' file and restart your docker-compose instance.

```bash
docker-compose up
```