# Database Migrations

This project now uses [Alembic](https://alembic.sqlalchemy.org/) for schema
changes. The configuration lives under `backend/alembic` and is wired to the
SQLAlchemy metadata defined in `app.db.database`.

## Running existing migrations

```bash
cd backend
source .venv/bin/activate    # if you haven't already
alembic upgrade head
```

`alembic` reads the `DATABASE_URL` environment variable. If it is not set, the
value from `alembic.ini` is used.

## Creating a new migration

```bash
cd backend
alembic revision -m "describe change"
# edit the new file under alembic/versions/...
alembic upgrade head
```

Please avoid creating ad-hoc `.sql` files; keeping all diffs in Alembic makes it
easy to replay changes across environments.
