#!/usr/bin/env bash
cd /app/aspects/migrations

echo "Running alembic $@"
alembic "$@"
