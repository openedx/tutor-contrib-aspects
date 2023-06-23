#!/usr/bin/env bash

python3 -m venv virtualenv
. virtualenv/bin/activate

echo "Installing dbt packages..."
pip install {{ DBT_PACKAGES }}

echo "Installing oars-dbt"
git clone -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }}

cd oars-dbt/oars || exit

echo "Installing dbt dependencies"
dbt deps --profiles-dir /app/aspects/scripts/aspects/

echo "Running dbt $*"
dbt "$@" --profiles-dir /app/aspects/scripts/aspects/
