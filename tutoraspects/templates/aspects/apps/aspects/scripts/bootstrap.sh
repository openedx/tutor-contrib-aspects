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

export branch=$(git -C aspects-dbt/ branch --show-current)
export repo=$(git -C aspects-dbt/ config --get remote.origin.url)
if [ "$DBT_BRANCH" != "$branch"  ] || [ "$DBT_REPOSITORY" != "$repo" ];
then
  rm -rf aspects-dbt

  echo "Installing aspects-dbt"
  echo "git clone -b ${DBT_BRANCH} ${DBT_REPOSITORY}"
  git clone -b ${DBT_BRANCH} ${DBT_REPOSITORY} aspects-dbt

  cd aspects-dbt

  if [ -e "./requirements.txt" ]
  then
    echo "Installing dbt python requirements"
    pip install -r ./requirements.txt
  else
    echo "No requirements.txt file found; skipping"
  fi

  echo "Installing dbt dependencies"
  dbt deps

fi

mkdir -p $DBT_STATE
