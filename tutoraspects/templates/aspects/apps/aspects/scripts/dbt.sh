#!/usr/bin/env bash


set -eo pipefail

## WARNING: If you modify this block, make sure to also update the
##          corresponding block in the init-aspects.sh file.

{% if DBT_SSH_KEY %}
mkdir -p /root/.ssh
echo "{{ DBT_SSH_KEY}}" | tr -d '\r' > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa
eval `ssh-agent -s`
ssh -o StrictHostKeyChecking=no git@github.com || true
ssh-add /root/.ssh/id_rsa
{% endif %}

rm -rf aspects-dbt

echo "Installing aspects-dbt"
echo "git clone -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }}"
git clone -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }} aspects-dbt

cd aspects-dbt

echo "Installing dbt python requirements"
pip install -r ./requirements.txt

export ASPECTS_EVENT_SINK_DATABASE={{ASPECTS_EVENT_SINK_DATABASE}}
export ASPECTS_XAPI_DATABASE={{ASPECTS_XAPI_DATABASE}}
export DBT_STATE={{ DBT_STATE_DIR }}
export ASPECTS_DATA_TTL_EXPRESSION="{{ ASPECTS_DATA_TTL_EXPRESSION }}"

echo "Installing dbt dependencies"
dbt deps --profiles-dir /app/aspects/dbt/

echo "Running dbt ${@:2}"

if [ "$1" == "True" ]
then
  echo "Requested to only run modified state, checking for ${DBT_STATE}/manifest.json"
fi

# If state exists and we've asked to only run changed files, add the flag
if [ "$1" == "True" ] && [ -e "${DBT_STATE}/manifest.json" ]
then
  echo "Found {{DBT_STATE_DIR}}/manifest.json so only running modified items and their downstreams"
  dbt "${@:2}" --profiles-dir /app/aspects/dbt/ -s state:modified+
else
  echo "Running command *without* state:modified+ this may take a long time."
  dbt "${@:2}" --profiles-dir /app/aspects/dbt/
fi

rm -rf ${DBT_STATE}/*
cp -r ./target/manifest.json ${DBT_STATE}
rm -rf aspects-dbt
