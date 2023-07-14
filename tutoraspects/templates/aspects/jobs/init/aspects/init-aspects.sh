#!/usr/bin/env bash

/app/aspects/scripts/alembic.sh upgrade head

/app/aspects/scripts/dbt.sh run
