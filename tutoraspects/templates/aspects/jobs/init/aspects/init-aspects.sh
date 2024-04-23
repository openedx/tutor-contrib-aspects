#!/usr/bin/env bash

set -eo pipefail

bash /app/aspects/scripts/alembic.sh upgrade head

bash /app/aspects/scripts/dbt.sh True run
