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

echo "Running schema creation scripts..."

{% if CLICKHOUSE_CLUSTER_NAME %}
{% set ON_CLUSTER = "ON CLUSTER '" ~ CLICKHOUSE_CLUSTER_NAME ~ "'" %}
{% else %}
{% set ON_CLUSTER = "" %}
{% endif %}

clickhouse client --user "{{ CLICKHOUSE_ADMIN_USER }}" --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" {% if CLICKHOUSE_SECURE_CONNECTION %} --secure {% else %} --port {{ CLICKHOUSE_INTERNAL_NATIVE_PORT }}{% endif %} --multiquery <<'EOF'
-- Create databases
CREATE DATABASE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }} {{ ON_CLUSTER }};
CREATE DATABASE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }} {{ ON_CLUSTER }};
CREATE DATABASE IF NOT EXISTS {{ ASPECTS_VECTOR_DATABASE }} {{ ON_CLUSTER }};
CREATE DATABASE IF NOT EXISTS {{ DBT_PROFILE_TARGET_DATABASE }} {{ ON_CLUSTER }};

-- Create various non-admin users reporting users
CREATE USER IF NOT EXISTS {{ ASPECTS_CLICKHOUSE_LRS_USER }} {{ ON_CLUSTER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_LRS_PASSWORD }}';
CREATE USER IF NOT EXISTS {{ ASPECTS_CLICKHOUSE_VECTOR_USER }} {{ ON_CLUSTER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_VECTOR_PASSWORD }}';
CREATE USER IF NOT EXISTS {{ ASPECTS_CLICKHOUSE_REPORT_USER }} {{ ON_CLUSTER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_REPORT_PASSWORD }}';
CREATE USER IF NOT EXISTS {{ ASPECTS_CLICKHOUSE_CMS_USER }} {{ ON_CLUSTER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_CMS_PASSWORD }}';

-- Update user passwords if they do exist
ALTER USER {{ ASPECTS_CLICKHOUSE_LRS_USER }} {{ ON_CLUSTER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_LRS_PASSWORD }}';
ALTER USER {{ ASPECTS_CLICKHOUSE_VECTOR_USER }} {{ ON_CLUSTER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_VECTOR_PASSWORD }}';
ALTER USER {{ ASPECTS_CLICKHOUSE_REPORT_USER }} {{ ON_CLUSTER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_REPORT_PASSWORD }}';
ALTER USER {{ ASPECTS_CLICKHOUSE_CMS_USER }} {{ ON_CLUSTER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_CMS_PASSWORD }}';

-- Grant permissions to the users
GRANT {{ ON_CLUSTER }} INSERT, SELECT ON {{ ASPECTS_XAPI_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_LRS_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON {{ ASPECTS_XAPI_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

GRANT {{ ON_CLUSTER }} INSERT, SELECT ON {{ ASPECTS_EVENT_SINK_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_CMS_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON {{ ASPECTS_EVENT_SINK_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

GRANT {{ ON_CLUSTER }} CREATE TABLE, DROP TABLE, CREATE VIEW, DROP VIEW, SELECT, INSERT, UPDATE, DELETE, dictGet ON {{ DBT_PROFILE_TARGET_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

GRANT {{ ON_CLUSTER }} SELECT, DROP TABLE, DROP VIEW ON {{ ASPECTS_XAPI_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';
GRANT {{ ON_CLUSTER }} INSERT, SELECT, DELETE ON {{ ASPECTS_EVENT_SINK_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_CMS_USER }}';
GRANT {{ ON_CLUSTER }} SELECT, dictGet ON {{ ASPECTS_EVENT_SINK_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';
GRANT {{ ON_CLUSTER }} INSERT, SELECT ON {{ ASPECTS_VECTOR_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_VECTOR_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON {{ ASPECTS_VECTOR_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON system.asynchronous_metrics TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON system.disks TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON system.events TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON system.metrics TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON system.replication_queue TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';
GRANT {{ ON_CLUSTER }} SELECT ON system.query_log TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

-- Altinity connector settings
CREATE DATABASE IF NOT EXISTS altinity_sink_connector {{ ON_CLUSTER }};

GRANT {{ ON_CLUSTER }} CREATE TABLE, DROP TABLE, CREATE VIEW, DROP VIEW, SELECT, INSERT, UPDATE, DELETE, dictGet ON altinity_sink_connector.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

GRANT {{ ON_CLUSTER }} CREATE TABLE, DROP TABLE, CREATE VIEW, DROP VIEW, SELECT, INSERT, UPDATE, DELETE, dictGet ON default.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

CREATE TABLE if not exists altinity_sink_connector.replica_source_info
(
    `id` String,
    `offset_key` String,
    `offset_val` String,
    `record_insert_ts` DateTime,
    `record_insert_seq` UInt64,
    `_version` UInt64 MATERIALIZED toUnixTimestamp64Nano(now64(9))
)
ENGINE = ReplacingMergeTree(_version)
ORDER BY id
SETTINGS index_granularity = 8198;

CREATE TABLE if not exists altinity_sink_connector.replicate_schema_history
(
    `id` VARCHAR(36) NOT NULL,
    `history_data` VARCHAR(65000),
    `history_data_seq` INTEGER,
    `record_insert_ts` TIMESTAMP NOT NULL,
    `record_insert_seq` INTEGER NOT NULL
)
ENGINE=ReplacingMergeTree(record_insert_seq) order by id;

-- Patch from clickhouse-extra-sql follows...
{{ patch("clickhouse-extra-sql") }}

EOF
