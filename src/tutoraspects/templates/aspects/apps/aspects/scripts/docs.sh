#!/usr/bin/env bash


set -eo pipefail

bash /app/aspects/scripts/bootstrap.sh

cd aspects-dbt
echo "Serving docs"

python3 /app/aspects/scripts/insert_data.py load

dbt docs generate

dbt docs serve --port 7000 --host 0.0.0.0
