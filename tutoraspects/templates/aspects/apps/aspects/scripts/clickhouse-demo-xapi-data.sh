#!/usr/bin/env bash
# Usage: clickhouse-demo-xapi-data.sh <load-db config> [<journeys config>]
set -eo pipefail
JOURNEYS_CONFIG=${2:-xapi-db-load-journeys.yaml}

echo "Loading demo xAPI data..."
cat $1
xapi-db-load load-db --config_file $1 || { ec=$?; printf '%s\n' "Error loading demo data!" >&2; exit $ec; }

echo "Loading learner journeys with known results..."
xapi-db-load journeys --config_file $JOURNEYS_CONFIG
xapi-db-load load-journeys --config_file $JOURNEYS_CONFIG

# The course structure and video models refresh on a timer and only look back a day for new
# video events, so bring them up to date with the history just loaded.
echo "Refreshing the course structure and video models..."
bash /app/aspects/scripts/dbt.sh False run -s dim_course_blocks+ fact_video_watch_intervals+

echo "Done."
