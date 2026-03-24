#!/usr/bin/env bash

set -eo pipefail

if [ -z "${DBT_SSH_KEY+x}" ]
then
  mkdir -p /root/.ssh
  echo "${DBT_SSH_KEY}" | tr -d '\r' > /root/.ssh/id_rsa
  chmod 600 /root/.ssh/id_rsa
  eval `ssh-agent -s`

  ssh -o StrictHostKeyChecking=no git@github.com || true
  ssh-add /root/.ssh/id_rsa
fi

git config --global --add safe.directory '*'

MOUNTED=false
if [ -d "aspects-dbt/.git" ]; then
  current_branch=$(git -C aspects-dbt/ branch --show-current)
  current_repo=$(git -C aspects-dbt/ config --get remote.origin.url)
  if [ ! -f "aspects-dbt/.git/shallow" ]; then
    MOUNTED=true
  fi
fi

if [ "$MOUNTED" = true ]; then
  echo "Using mounted repo (branch: ${current_branch})"
else
  # Only re-clone if branch/repo differ or directory is missing
  if [ ! -d "aspects-dbt/.git" ] \
    || [ "${DBT_BRANCH}" != "${current_branch}" ] \
    || [ "${DBT_REPOSITORY}" != "${current_repo}" ]; then

    rm -rf aspects-dbt

    echo "Installing aspects-dbt"
    echo "git clone -b ${DBT_BRANCH} ${DBT_REPOSITORY}"
    git clone -b "${DBT_BRANCH}" "${DBT_REPOSITORY}" aspects-dbt
  else
    echo "Using existing cloned repo (branch: ${current_branch})"
  fi
fi

cd aspects-dbt

if [ -e "./requirements.txt" ]; then
  echo "Installing dbt python requirements"
  uv pip install -r ./requirements.txt --system
else
  echo "No requirements.txt file found; skipping"
fi

echo "Installing dbt dependencies"
dbt deps

mkdir -p "${DBT_STATE}"