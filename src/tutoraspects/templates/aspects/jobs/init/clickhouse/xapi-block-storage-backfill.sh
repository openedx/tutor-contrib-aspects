#!/bin/bash
set -e

echo "Initialising xAPI backfill..."
ch_connection_max_attempts=10
ch_connection_attempt=0
until clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" {% if CLICKHOUSE_SECURE_CONNECTION %} --secure {% else %} --port {{ CLICKHOUSE_INTERNAL_NATIVE_PORT }}{% endif %} -q 'exit'
do
    ch_connection_attempt=$(expr $ch_connection_attempt + 1)
    echo "    [$ch_connection_attempt/$ch_connection_max_attempts] Waiting for Clickhouse service (this may take a while)..."
    if [ $ch_connection_attempt -eq $ch_connection_max_attempts ]
    then
      echo "Clickhouse connection error" 1>&2
      exit 1
    fi
    sleep 10
done
echo "Clickhouse is up and running"

XAPI_S3_PATH="{{ ASPECTS_XAPI_S3_ENDPOINT }}/{{ ASPECTS_XAPI_S3_BUCKET }}/{{XAPI_S3_PATH}}"

echo "Backfilling xAPI events from: ${XAPI_S3_PATH}"

clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" {% if CLICKHOUSE_SECURE_CONNECTION %} --secure {% else %} --port {{ CLICKHOUSE_INTERNAL_NATIVE_PORT }}{% endif %} --multiquery <<EOF
SELECT 'Files to be read:' AS status, count() AS files FROM s3('${XAPI_S3_PATH}', '{{ ASPECTS_XAPI_S3_ACCESS_KEY }}', '{{ ASPECTS_XAPI_S3_SECRET_KEY }}', 'One');
SELECT 'Current events:' AS status, count() AS rows FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }};

INSERT INTO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
SELECT event_id, parseDateTime64BestEffort(emission_time), event
FROM s3('${XAPI_S3_PATH}', '{{ ASPECTS_XAPI_S3_ACCESS_KEY }}', '{{ ASPECTS_XAPI_S3_SECRET_KEY }}', 'JSONEachRow', 'event_id String, emission_time String, event String', 'zstd');

SELECT 'Current events:' AS status, count() AS rows FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }};
EOF

echo "xAPI backfill complete!"
