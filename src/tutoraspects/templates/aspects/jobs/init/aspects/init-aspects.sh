#!/usr/bin/env bash

set -e

bash /app/aspects/scripts/alembic.sh upgrade head

bash /app/aspects/scripts/dbt.sh True run
