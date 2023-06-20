#!/usr/bin/env bash

python3 -m venv virtualenv
. virtualenv/bin/activate

echo "Installing dbt packages..."
pip install pip install {{ DBT_PACKAGES }}

echo "Installing oars-dbt"
git clone {{ DBT_REPOSITORY }}

cd oars-dbt/oars || exit

echo "Installing dbt dependencies"
dbt deps --profiles-dir /app/oars/scripts/oars/

echo "Running dbt $*"
dbt "$@" --profiles-dir /app/oars/scripts/oars/
