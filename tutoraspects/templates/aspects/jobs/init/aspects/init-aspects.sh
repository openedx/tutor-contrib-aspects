#!/usr/bin/env bash

chmod +x /app/aspects/scripts/alembic.sh
/app/aspects/scripts/alembic.sh upgrade head

chmod +x /app/aspects/scripts/dbt.sh
/app/aspects/scripts/dbt.sh run
