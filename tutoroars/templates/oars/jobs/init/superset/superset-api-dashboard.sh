#!/usr/bin/env bash
set -e

#
# Always install local overrides first
#
/usr/bin/env bash /app/docker/docker-bootstrap.sh

echo "\n\nInstall zip\n\n"
apt update
apt install zip unzip

cd /app/oars/data/
echo "\n\nListing mounted files\n\n"
ls -R superset/

echo "\n\nCompressing superset folder\n\n"
zip -r superset.zip superset -i superset/metadata.yaml -i superset/dashboards/*.yaml -i superset/databases/*.yaml -i superset/datasets/OpenedX_MySQL/*.yaml -i superset/datasets/OpenedX_Clickhouse/*.yaml -i superset/charts/*.yaml

echo "\n\nListing files in zip\n\n"
unzip -l superset.zip

echo "\n\nImporting zip file\n\n"
superset import-dashboards -p superset.zip
