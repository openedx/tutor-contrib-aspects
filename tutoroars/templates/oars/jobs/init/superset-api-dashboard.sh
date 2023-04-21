#!/usr/bin/env bash
set -e

pip install -r /app/oars/pythonpath/requirements.txt
python /app/oars/pythonpath/superset-dashboard.py && echo "Success"
