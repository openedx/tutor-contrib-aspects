#!/usr/bin/env bash

python3 -m venv virtualenv
. virtualenv/bin/activate

echo "Installing dbt packages..."

pip install -r /app/aspects/scripts/aspects/requirements.txt

echo "Installing aspects-dbt"
git clone -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }}

cd {{ DBT_REPOSITORY_PATH }} || exit

echo "Installing dbt dependencies"
dbt deps --profiles-dir /app/aspects/scripts/aspects/

echo "Running dbt"
dbt run --profiles-dir /app/aspects/scripts/aspects/
