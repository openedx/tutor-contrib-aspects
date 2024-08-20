#!/usr/bin/env bash


set -eo pipefail

bash /app/aspects/scripts/bootstrap.sh

cd /app/aspects-dbt
echo "Running ${@:2}"

python3 /app/aspects/scripts/insert_data.py load

dbt parse

# If state exists and we've asked to only run changed files, add the flag
if [ "$1" == "True" ] && [ -e "${DBT_STATE}/manifest.json" ]
then
  echo "Found ${DBT_STATE}/manifest.json so only running modified items and their downstreams"
  dbt ${@:2} -s "state:modified+"
else
  echo "Running command *without* state:modified+ this may take a long time."
  dbt ${@:2}
fi

if [ -e "target/manifest.json" ]
then
  echo "Updating dbt state..."
  cp target/manifest.json state
  python3 /app/aspects/scripts/insert_data.py sink
fi

rm -rf aspects-dbt
