#!/usr/bin/env bash
set -e

VENV_DIR=/opt/venv

python -m venv $VENV_DIR
$VENV_DIR/bin/pip install -r /app/oars/pythonpath/requirements.txt
$VENV_DIR/bin/python /app/oars/pythonpath/superset-dashboard.py && echo "Success"
