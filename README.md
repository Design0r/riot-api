# Riot API Client with DB caching

## Requirements

- Python 3.13
- PostgreSQL or Docker
- uv

## Installation

1. Clone the Repository

```bash
https://github.com/Design0r/riot-api.git
```

2. Create .env from .env.template

3. Run PostgreSQL in docker

```bash
docker compose up --build -d
```

4. Run migrations

```bash
cd riotapi
uv run manage.py migrate
uv run manage.py initadmin
```

## Usage

### Check the DB entries in the django admin dashboard.

```bash
uv run manage.py runserver
```

### Run custom scripts with the django_prelude.py import

example main.py

```bash
uv run main.py
```
