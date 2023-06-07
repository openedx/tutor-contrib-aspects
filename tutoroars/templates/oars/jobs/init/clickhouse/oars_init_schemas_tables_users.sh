echo "Running schema creation scripts..."
clickhouse client --user "{{ CLICKHOUSE_ADMIN_USER }}" --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" {% if CLICKHOUSE_SECURE_CONNECTION %} --secure {% else %} --port {{ CLICKHOUSE_PORT }}{% endif %} --multiquery <<'EOF'
-- Allow JSON fields
SET allow_experimental_object_type=1;

-- Create various non-admin users reporting users
CREATE USER IF NOT EXISTS {{ OARS_CLICKHOUSE_LRS_USER }} IDENTIFIED WITH sha256_password BY '{{ OARS_CLICKHOUSE_LRS_PASSWORD }}';
CREATE USER IF NOT EXISTS {{ OARS_CLICKHOUSE_REPORT_USER }} IDENTIFIED WITH sha256_password BY '{{ OARS_CLICKHOUSE_REPORT_PASSWORD }}';
CREATE USER IF NOT EXISTS {{ OARS_CLICKHOUSE_CMS_USER }} IDENTIFIED WITH sha256_password BY '{{ OARS_CLICKHOUSE_CMS_PASSWORD }}';

-- Update user passwords if they do exist
ALTER USER {{ OARS_CLICKHOUSE_LRS_USER }} IDENTIFIED WITH sha256_password BY '{{ OARS_CLICKHOUSE_LRS_PASSWORD }}';
ALTER USER {{ OARS_CLICKHOUSE_REPORT_USER }} IDENTIFIED WITH sha256_password BY '{{ OARS_CLICKHOUSE_REPORT_PASSWORD }}';
ALTER USER {{ OARS_CLICKHOUSE_CMS_USER }} IDENTIFIED WITH sha256_password BY '{{ OARS_CLICKHOUSE_CMS_PASSWORD }}';

-- Create the terrible user defined function to parse the org out of course URLs
-- if we need to update this just add a COALESCE around the whole thing and put in
-- additional cases wrapped in nullIf's until we get them all. Other things we may find in these URLs eventually:
-- i4x://{org}/{rest of key}  Old Mongo usage keys
-- c4x://{org}/{rest of key}  Old Mongo assets
-- {org}/{rest of key} Old Mongo course keys
CREATE OR REPLACE FUNCTION get_org_from_course_url AS (course_url) ->
  nullIf(EXTRACT(course_url, 'course-v1:([a-zA-Z0-9]*)'), '')
;

-- Create the xapi schema if it doesn't exist
CREATE DATABASE IF NOT EXISTS {{ OARS_XAPI_DATABASE }};

-- Raw table that Ralph writes to
CREATE TABLE IF NOT EXISTS {{ OARS_XAPI_DATABASE }}.{{ OARS_RAW_XAPI_TABLE }}  (
    event_id UUID NOT NULL,
    emission_time DateTime64(6) NOT NULL,
    event JSON NOT NULL,
    event_str String NOT NULL
) ENGINE MergeTree
ORDER BY (emission_time, event_id)
PRIMARY KEY (emission_time, event_id);

-- Processed table that Superset reads from
CREATE TABLE IF NOT EXISTS {{ OARS_XAPI_DATABASE }}.{{ OARS_XAPI_TABLE }} (
    event_id UUID NOT NULL,
    verb_id String NOT NULL,
    actor_id String NOT NULL,
    object_id String NOT NULL,
    org String NOT NULL,
    course_id String NOT NULL,
    emission_time DateTime64(6) NOT NULL,
    event_str String NOT NULL
) ENGINE MergeTree
ORDER BY (org, course_id, verb_id, actor_id, emission_time, event_id)
PRIMARY KEY (org, course_id, verb_id, actor_id, emission_time, event_id);

-- Materialized view that moves data from the raw table to processed table
CREATE MATERIALIZED VIEW IF NOT EXISTS {{ OARS_XAPI_DATABASE }}.{{ OARS_XAPI_TRANSFORM_MV }}
    TO {{ OARS_XAPI_DATABASE }}.{{ OARS_XAPI_TABLE }} AS
    SELECT
    event_id as event_id,
    JSON_VALUE(event_str, '$.verb.id') as verb_id,
    JSON_VALUE(event_str, '$.actor.account.name') as actor_id,
    JSON_VALUE(event_str, '$.object.id') as object_id,
    -- If the contextActivities parent is a course, use that. Otherwise use the object id for the course id
    if(
        JSON_VALUE(
            event_str,
            '$.context.contextActivities.parent[0].definition.type')
                = 'http://adlnet.gov/expapi/activities/course',
            JSON_VALUE(event_str, '$.context.contextActivities.parent[0].id'),
            JSON_VALUE(event_str, '$.object.id')
        ) as course_id,
    get_org_from_course_url(course_id) as org,
    emission_time as emission_time,
    event_str as event_str
    FROM {{ OARS_XAPI_DATABASE }}.{{ OARS_RAW_XAPI_TABLE }};


-- Create the event sink schema if it doesn't exist
CREATE DATABASE IF NOT EXISTS {{ OARS_EVENT_SINK_DATABASE }};

CREATE TABLE IF NOT EXISTS {{ OARS_EVENT_SINK_DATABASE }}.{{ OARS_EVENT_SINK_OVERVIEWS_TABLE }}
(
    org String NOT NULL,
    course_key String NOT NULL,
    display_name String NOT NULL,
    course_start String NOT NULL,
    course_end String NOT NULL,
    enrollment_start String NOT NULL,
    enrollment_end String NOT NULL,
    self_paced BOOL NOT NULL,
    course_data_json String NOT NULL,
    created String NOT NULL,
    modified String NOT NULL,
    dump_id UUID NOT NULL,
    time_last_dumped String NOT NULL
) engine = MergeTree
    PRIMARY KEY (org, course_key, modified, time_last_dumped)
    ORDER BY (org, course_key, modified, time_last_dumped);

CREATE TABLE IF NOT EXISTS {{ OARS_EVENT_SINK_DATABASE }}.{{ OARS_EVENT_SINK_NODES_TABLE }}
(
    org String NOT NULL,
    course_key String NOT NULL,
    location String NOT NULL,
    display_name String NOT NULL,
    xblock_data_json String NOT NULL,
    order Int32 default 0,
    edited_on String NOT NULL,
    dump_id UUID NOT NULL,
    time_last_dumped String NOT NULL
) engine = MergeTree
    PRIMARY KEY (org, course_key, location, edited_on)
    ORDER BY (org, course_key, location, edited_on, order);

CREATE TABLE IF NOT EXISTS {{ OARS_EVENT_SINK_DATABASE }}.{{ OARS_EVENT_SINK_RELATIONSHIPS_TABLE }}
(
    course_key String NOT NULL,
    parent_location String NOT NULL,
    child_location String NOT NULL,
    order Int32 NOT NULL,
    dump_id UUID NOT NULL,
    time_last_dumped String NOT NULL
) engine = MergeTree
    PRIMARY KEY (course_key, parent_location, child_location, time_last_dumped)
    ORDER BY (course_key, parent_location, child_location, time_last_dumped, order);


-- Grant permissions to the users
GRANT INSERT, SELECT ON {{ OARS_XAPI_DATABASE }}.* TO '{{ OARS_CLICKHOUSE_LRS_USER }}';
GRANT SELECT ON {{ OARS_XAPI_DATABASE }}.* TO '{{ OARS_CLICKHOUSE_REPORT_USER }}';

GRANT INSERT, SELECT ON {{ OARS_EVENT_SINK_DATABASE }}.* TO '{{ OARS_CLICKHOUSE_CMS_USER }}';
GRANT SELECT ON {{ OARS_EVENT_SINK_DATABASE }}.* TO '{{ OARS_CLICKHOUSE_REPORT_USER }}';

EOF
