#!/usr/bin/env bash

python3 -m venv virtualenv
. virtualenv/bin/activate

echo "Installing dbt packages..."

pip install -r /app/aspects/dbt/requirements.txt

echo "Installing aspects-dbt"
git clone -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }}

cd {{ DBT_REPOSITORY_PATH }} || exit

echo "Installing dbt dependencies"
dbt deps --profiles-dir /app/aspects/dbt/

echo "Running dbt $*"
dbt "$@" --profiles-dir /app/aspects/dbt/
