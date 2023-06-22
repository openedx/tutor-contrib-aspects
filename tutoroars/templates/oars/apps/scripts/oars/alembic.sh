#!/usr/bin/env bash

python3 -m venv virtualenv
. virtualenv/bin/activate

cd /app/oars/clickhouse/migrations

echo "Installing packages..."
pip install -r requirements.txt

echo "Running alembic $*"
alembic "$@"
