echo "Initialising Clickhouse..."
ch_connection_max_attempts=10
ch_connection_attempt=0
until clickhouse client --user {{ CLICKHOUSE_ADMIN_USER }} --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" {% if CLICKHOUSE_SECURE_CONNECTION %} --secure {% else %} --port {{ CLICKHOUSE_CLIENT_PORT }}{% endif %} -q 'exit'
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
clickhouse client --user "{{ CLICKHOUSE_ADMIN_USER }}" --password="{{ CLICKHOUSE_ADMIN_PASSWORD }}" --host "{{ CLICKHOUSE_HOST }}" {% if CLICKHOUSE_SECURE_CONNECTION %} --secure {% else %} --port {{ CLICKHOUSE_CLIENT_PORT }}{% endif %} --multiquery <<'EOF'
-- Allow JSON fields
SET allow_experimental_object_type=1;

-- Create various non-admin users reporting users
CREATE USER IF NOT EXISTS {{ ASPECTS_CLICKHOUSE_LRS_USER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_LRS_PASSWORD }}';
CREATE USER IF NOT EXISTS {{ ASPECTS_CLICKHOUSE_VECTOR_USER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_VECTOR_PASSWORD }}';
CREATE USER IF NOT EXISTS {{ ASPECTS_CLICKHOUSE_REPORT_USER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_REPORT_PASSWORD }}';
CREATE USER IF NOT EXISTS {{ ASPECTS_CLICKHOUSE_CMS_USER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_CMS_PASSWORD }}';

-- Update user passwords if they do exist
ALTER USER {{ ASPECTS_CLICKHOUSE_LRS_USER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_LRS_PASSWORD }}';
ALTER USER {{ ASPECTS_CLICKHOUSE_VECTOR_USER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_VECTOR_PASSWORD }}';
ALTER USER {{ ASPECTS_CLICKHOUSE_REPORT_USER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_REPORT_PASSWORD }}';
ALTER USER {{ ASPECTS_CLICKHOUSE_CMS_USER }} IDENTIFIED WITH sha256_password BY '{{ ASPECTS_CLICKHOUSE_CMS_PASSWORD }}';

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
CREATE DATABASE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }};

-- Raw table that Ralph writes to
CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}  (
    event_id UUID NOT NULL,
    emission_time DateTime64(6) NOT NULL,
    event JSON NOT NULL,
    event_str String NOT NULL
) ENGINE MergeTree
ORDER BY (emission_time, event_id)
PRIMARY KEY (emission_time, event_id);

-- Processed table that Superset reads from
CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }} (
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
CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TRANSFORM_MV }}
    TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }} AS
    SELECT
    event_id as event_id,
    JSON_VALUE(event_str, '$.verb.id') as verb_id,
    COALESCE(
        NULLIF(JSON_VALUE(event_str, '$.actor.account.name'), ''),
        NULLIF(JSON_VALUE(event_str, '$.actor.mbox'), ''),
        JSON_VALUE(event_str, '$.actor.mbox_sha1sum')
    ) as actor_id,
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
    FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }};

-- MV target table for enrollment xAPI events
CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }} (
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_id` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `enrollment_mode` LowCardinality(String)
) ENGINE = MergeTree
PRIMARY KEY (org, course_id)
ORDER BY (org, course_id, actor_id, enrollment_mode, emission_time);

-- Materialized view that moves data from the processed xAPI table to
-- the enrollment events table
CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_TRANSFORM_MV }}
    TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }} AS
SELECT
    event_id,
    emission_time,
    actor_id,
    object_id,
    course_id,
    org,
    verb_id,
    JSON_VALUE(event_str, '$.object.definition.extensions."https://w3id.org/xapi/acrossx/extensions/type"') AS enrollment_mode
FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
WHERE verb_id IN (
  'http://adlnet.gov/expapi/verbs/registered',
  'http://id.tincanapi.com/verb/unregistered'
);


-- MV target table for video playback xAPI events
CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }} (
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_id` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `video_position` Float32 NOT NULL
) ENGINE = MergeTree
PRIMARY KEY (org, course_id, verb_id)
ORDER BY (org, course_id, verb_id, actor_id);

-- Materialized view that moves data from the processed xAPI table to
-- the video playback events table
CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_TRANSFORM_MV }}
    TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }} AS
SELECT
    event_id,
    emission_time,
    actor_id,
    object_id,
    course_id,
    org,
    verb_id,
    cast(coalesce(
        nullif(JSON_VALUE(event_str, '$.result.extensions."https://w3id.org/xapi/video/extensions/time"'), ''),
        nullif(JSON_VALUE(event_str, '$.result.extensions."https://w3id.org/xapi/video/extensions/time-from"'), ''),
        '0.0'
    ) as Float32) as video_position
FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
WHERE verb_id IN (
  'http://adlnet.gov/expapi/verbs/completed',
  'http://adlnet.gov/expapi/verbs/initialized',
  'http://adlnet.gov/expapi/verbs/terminated',
  'https://w3id.org/xapi/video/verbs/paused',
  'https://w3id.org/xapi/video/verbs/played',
  'https://w3id.org/xapi/video/verbs/seeked'
);


-- MV target table for problem interaction xAPI events
CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }} (
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_id` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `responses` String,
    `scaled_score` String,
    `success` Bool,
    `interaction_type` LowCardinality(String),
    `attempts` Int16
) ENGINE = MergeTree
PRIMARY KEY (org, course_id, verb_id)
ORDER BY (org, course_id, verb_id, actor_id);


-- Materialized view that moves data from the processed xAPI table to
-- the problem events table
-- n.b. this query omits browser problem_checked events, as they do not
-- contain any information that the server events don't have and including
-- them would heavily skew the distribution of values in the problem
-- response fields (responses, scaled_score, etc)
CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }}
    TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }} AS
select
    event_id,
    emission_time,
    actor_id,
    object_id,
    course_id,
    org,
    verb_id,
    JSON_VALUE(event_str, '$.result.response') as responses,
    JSON_VALUE(event_str, '$.result.score.scaled') as scaled_score,
    if(
        verb_id = 'https://w3id.org/xapi/acrossx/verbs/evaluated',
        cast(JSON_VALUE(event_str, '$.result.success') as Bool),
        false
    ) as success,
    JSON_VALUE(event_str, '$.object.definition.interactionType') as interaction_type,
    if(
        verb_id = 'https://w3id.org/xapi/acrossx/verbs/evaluated',
        cast(JSON_VALUE(event_str, '$.object.definition.extensions."http://id.tincanapi.com/extension/attempt-id"') as Int16),
        0
    ) as attempts
from
    {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
where
    verb_id in (
        'https://w3id.org/xapi/acrossx/verbs/evaluated',
        'http://adlnet.gov/expapi/verbs/passed',
        'http://adlnet.gov/expapi/verbs/asked'
    );



-- MV target table for navigation xAPI events
CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }} (
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_id` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `object_type` LowCardinality(String) NOT NULL,
    `starting_position` Int16,
    `ending_point` String
) ENGINE = MergeTree
PRIMARY KEY (org, course_id, object_type)
ORDER BY (org, course_id, object_type, actor_id);


-- Materialized view that moves data from the processed xAPI table to
-- the enrollment events table
CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_TRANSFORM_MV }}
TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }} AS
SELECT
    event_id,
    emission_time,
    actor_id,
    object_id,
    course_id,
    org,
    verb_id,
    JSON_VALUE(event_str, '$.object.definition.type') AS object_type,
    -- clicking a link and selecting a module outline have no starting-position field
    if (
        object_type in (
            'http://adlnet.gov/expapi/activities/link',
            'http://adlnet.gov/expapi/activities/module'
        ),
        0,
        cast(JSON_VALUE(
            event_str,
            '$.context.extensions."http://id.tincanapi.com/extension/starting-position"'
        ) as Int16)
    ) AS starting_position,
    JSON_VALUE(
        event_str,
        '$.context.extensions."http://id.tincanapi.com/extension/ending-point"'
    ) AS ending_point
FROM
    {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
WHERE verb_id IN (
    'https://w3id.org/xapi/dod-isd/verbs/navigated'
);



-- Create the event sink schema if it doesn't exist
CREATE DATABASE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }};

CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_OVERVIEWS_TABLE }}
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

CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
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

CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_RELATIONSHIPS_TABLE }}
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
GRANT INSERT, SELECT ON {{ ASPECTS_XAPI_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_LRS_USER }}';
GRANT SELECT ON {{ ASPECTS_XAPI_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

GRANT INSERT, SELECT ON {{ ASPECTS_EVENT_SINK_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_CMS_USER }}';
GRANT SELECT ON {{ ASPECTS_EVENT_SINK_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

-- Create dbt database and grant permissions
CREATE DATABASE IF NOT EXISTS {{ DBT_PROFILE_TARGET_DATABASE }};
GRANT CREATE TABLE, DROP TABLE, CREATE VIEW, DROP VIEW, SELECT, INSERT, UPDATE, DELETE ON {{ DBT_PROFILE_TARGET_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

-- Vector database and tables
-- This is just temporary so that Vector has a place to write. Once these are all Alembic migrations
-- it will be a lot more sane.
CREATE DATABASE IF NOT EXISTS {{ ASPECTS_VECTOR_DATABASE }};

CREATE TABLE IF NOT EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE }}
(
    `time` DateTime,
    `message` String
)
ENGINE MergeTree
ORDER BY time;

CREATE TABLE IF NOT EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_XAPI_TABLE }}
(
    event_id      UUID,
    emission_time DateTime64(6),
    event_str     String
)
engine = MergeTree
PRIMARY KEY (emission_time)
ORDER BY (emission_time, event_id);

GRANT INSERT, SELECT ON {{ ASPECTS_VECTOR_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_VECTOR_USER }}';
GRANT SELECT ON {{ ASPECTS_VECTOR_DATABASE }}.* TO '{{ ASPECTS_CLICKHOUSE_REPORT_USER }}';

EOF
