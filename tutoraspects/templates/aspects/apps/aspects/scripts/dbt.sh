#!/usr/bin/env bash


set -eo pipefail

echo "Running ${@:2}"

if [ "$1" == "True" ]
then
  echo "Requested to only run modified state, checking for ${DBT_STATE}/manifest.json"
fi

# If state exists and we've asked to only run changed files, add the flag
if [ "$1" == "True" ] && [ -e "${DBT_STATE}/manifest.json" ]
then
  echo "Found {{DBT_STATE_DIR}}/manifest.json so only running modified items and their downstreams"
  ${@:2} -s state:modified+
else
  echo "Running command *without* state:modified+ this may take a long time."
  ${@:2}
fi

if [ -e "./target/manifest.json" ]
then
  echo "Updating dbt state..."
  rm -rf ${DBT_STATE}/*
  cp -r ./target/manifest.json ${DBT_STATE}
fi

rm -rf aspects-dbt
