#!/usr/bin/env bash

## WARNING: If you modify this block, make sure to also update the
##          corresponding block in the init-aspects.sh file.

echo "Installing dbt packages..."

pip install -r /app/aspects/dbt/requirements.txt

rm -rf {{ DBT_REPOSITORY_PATH }}

echo "Installing aspects-dbt"
echo "git clone -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }}"
git clone -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }}

cd {{ DBT_REPOSITORY_PATH }} || exit

export ASPECTS_EVENT_SINK_DATABASE={{ASPECTS_EVENT_SINK_DATABASE}}

echo "Installing dbt dependencies"
dbt deps --profiles-dir /app/aspects/dbt/

echo "Running dbt $*"
dbt "$@" --profiles-dir /app/aspects/dbt/

rm -rf {{ DBT_REPOSITORY_PATH }}
