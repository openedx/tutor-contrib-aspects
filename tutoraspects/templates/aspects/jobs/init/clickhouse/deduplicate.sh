echo "Initialising Clickhouse..."
ch_connection_max_attempts=10
ch_connection_attempt=0
until clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" {% if CLICKHOUSE_SECURE_CONNECTION %} --secure {% else %} --port {{ CLICKHOUSE_INTERNAL_NATIVE_PORT }}{% endif %} -q 'exit'
do
    ch_connection_attempt=$(expr $ch_connection_attempt + 1)
    echo "    [$ch_connection_attempt/$ch_connection_max_attempts] Waiting for Clickhouse service (this may take a while)..."
    if [ $ch_connection_attempt -eq $ch_connection_max_attempts ]
    then
      echo "Clickhouse initialisation error" 1>&2
      exit 1
    fi
    sleep 10
done
echo "Clickhouse is up and running"

echo "Running deduplication script..."

clickhouse client --user "{{ CLICKHOUSE_ADMIN_USER }}" --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" {% if CLICKHOUSE_SECURE_CONNECTION %} --secure {% else %} --port {{ CLICKHOUSE_INTERNAL_NATIVE_PORT }}{% endif %} --multiquery <<'EOF'
-- Optimize final
OPTIMIZE TABLE {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_RAW_XAPI_TABLE}} FINAL;
OPTIMIZE TABLE {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_ENROLLMENT_EVENTS_TABLE}} FINAL;
OPTIMIZE TABLE {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_XAPI_TABLE}} FINAL;
OPTIMIZE TABLE {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_NAVIGATION_EVENTS_TABLE}} FINAL;
OPTIMIZE TABLE {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_PROBLEM_EVENTS_TABLE}} FINAL;
OPTIMIZE TABLE {{ASPECTS_XAPI_DATABASE}}.{{ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE}} FINAL;

EOF
