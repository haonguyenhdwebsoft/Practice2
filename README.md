# Practice2

## Prerequisites
- Python 3.7.8 (Ignore if using Docker)
- Virtualenv (Ignore if using Docker)
- Postgres 12 (Ignore if using Docker)
- Docker (Optional)
- Docker Compose (Optional)

## Using Virtualenv
```bash
# 1. Create and activate virtualenv
$ python -m venv .venv
$ .venv\Scripts\activate.bat

# 2. Install dependencies
$ pip install --upgrade pip
$ pip install -r requirements/local.txt

# 3. Go to project folder
$ cd sample

# 4. Migrate database
$ python manage.py migrate

# 5. Start Django
$ python manage.py runserver 0.0.0.0:8000
```

## Build and Start App using Docker
```bash
# Build
$ docker-compose up -d db

# Start container
$ docker compose up

```

## Django
- URL: http://localhost:8000/api

## Swagger Document
- URL: http://localhost:8000/swagger

