#!/usr/bin/env bash

set -eo pipefail

mkdir -p /app/assets/
cd /app/assets/
rm -rf superset

mkdir superset

date=$(date -u +"%Y-%m-%dT%H:%M:%S.%6N+00:00")
echo "version: 1.0.0
type: assets
timestamp: '$date'" > superset/metadata.yaml

python /app/pythonpath/create_assets.py

rm -rf /app/assets/superset
