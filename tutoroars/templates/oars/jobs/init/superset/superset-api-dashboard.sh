#!/usr/bin/env bash
set -e

#
# Always install local overrides first
#
/usr/bin/env bash /app/docker/docker-bootstrap.sh

apt update
apt install zip unzip

rm -rf /app/assets/superset

cd /app/assets/

python /app/pythonpath/create_assets.py

date=$(date -u +"%Y-%m-%dT%H:%M:%S.%6N+00:00") 

echo "version: 1.0.0
type: Dashboard
timestamp: '$date'" > superset/metadata.yaml

echo "\n\nCompressing superset folder\n\n"
zip -r superset.zip superset

echo "\n\nListing files in zip\n\n"
unzip -l superset.zip

echo "\n\nImporting zip file\n\n"
superset import-dashboards -p superset.zip
