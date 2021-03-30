# Certificate Checker

Checkout [danieldaeschle/morpheus-certificates](https://github.com/danieldaeschle/morpheus-certificates).

## Installation
First you need to install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)  
After you have started the services (`docker-compose up -d`), you can collect the static files and create an superuser:  
```bash
# collect static files
docker-compose exec -u0 cert-checker /bin/sh -c 'python manage.py collectstatic --no-input'

# create superuser
docker-compose exec cert-checker /bin/sh -c 'python manage.py createsuperuser --username=admin --email=admin@example.de'
```

Afterwards you can access the application: [http://localhost:8080](http://localhost:8080)  
You can change the port inside the [`docker-compose.yml`](./docker-compose.yml#L29)
