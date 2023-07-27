Alembic migrations for Aspects
===============================

Alembic is a migration tool for SQLAlchemy. It is used to manage the clickhouse database
schema for the Aspects project.

For more information about Alembic, see https://alembic.sqlalchemy.org/en/latest/

Aspects interface for Alembic
-----------------------------

The Aspects project provides a custom interface for Alembic. This interface is
available in the command line with the subcommand ``tutor local|dev do alembic -c "custom command"``.

For example, to run the command ``alembic upgrade head`` in the dev environment, you would run::

    tutor dev do alembic -c "upgrade head"

Common Alembic operations
-------------------------

The following are some common Alembic operations.

Create a new migration::

    tutor dev do alembic -c "revision -m 'migration message'"

Run migrations::

    tutor dev do alembic -c "upgrade head"

Rollback migrations::

    tutor dev do alembic -c "downgrade -1"

