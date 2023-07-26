#!/usr/bin/env bash

## WARNING: If you modify this block, make sure to also update the
##          corresponding block in the init-aspects.sh file.

cd /app/aspects/migrations

echo "Running alembic $@"
alembic "$@"
