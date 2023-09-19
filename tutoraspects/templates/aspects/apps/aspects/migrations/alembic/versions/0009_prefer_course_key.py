from dataclasses import dataclass

from alembic import op

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


@dataclass
class MvMigration:
    table_name: str
    old_ddl: str
    new_ddl: str
    mv_name: str
    old_mv_query: str
    new_mv_query: str


OLD_ENROLLMENT_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }} 
    {on_cluster}
    (
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_id` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `enrollment_mode` LowCardinality(String)
) ENGINE = {engine}
PRIMARY KEY (org, course_id)
ORDER BY (org, course_id, actor_id, enrollment_mode, emission_time);
"""

NEW_ENROLLMENT_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }}
    {on_cluster} 
    (
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_key` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `enrollment_mode` LowCardinality(String)
) ENGINE = {engine}
PRIMARY KEY (org, course_key)
ORDER BY (org, course_key, actor_id, enrollment_mode, emission_time);
"""

OLD_ENROLLMENT_QUERY = """
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
"""

NEW_ENROLLMENT_QUERY = """
SELECT
    event_id,
    emission_time,
    actor_id,
    object_id,
    splitByString('/', course_id)[-1] AS course_key,
    org,
    verb_id,
    JSON_VALUE(event_str, '$.object.definition.extensions."https://w3id.org/xapi/acrossx/extensions/type"') AS enrollment_mode
FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
WHERE verb_id IN (
    'http://adlnet.gov/expapi/verbs/registered',
    'http://id.tincanapi.com/verb/unregistered'
);
"""

OLD_VIDEO_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}
{on_cluster}
(
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_id` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `video_position` Float32 NOT NULL
) ENGINE = {engine}
PRIMARY KEY (org, course_id, verb_id)
ORDER BY (org, course_id, verb_id, actor_id);
"""

NEW_VIDEO_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }} 
{on_cluster}
(
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_key` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `video_position` Float32 NOT NULL
) ENGINE = {engine}
PRIMARY KEY (org, course_key, verb_id)
ORDER BY (org, course_key, verb_id, actor_id);
"""

OLD_VIDEO_QUERY = """
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
"""

NEW_VIDEO_QUERY = """
SELECT
    event_id,
    emission_time,
    actor_id,
    object_id,
    splitByString('/', course_id)[-1] AS course_key,
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
"""

OLD_PROBLEM_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }} 
{on_cluster}
(
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
) ENGINE = {engine}
PRIMARY KEY (org, course_id, verb_id)
ORDER BY (org, course_id, verb_id, actor_id);
"""

NEW_PROBLEM_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }} 
{on_cluster}
(
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_key` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `responses` String,
    `scaled_score` String,
    `success` Bool,
    `interaction_type` LowCardinality(String),
    `attempts` Int16
) ENGINE = {engine}
PRIMARY KEY (org, course_key, verb_id)
ORDER BY (org, course_key, verb_id, actor_id);
"""

OLD_PROBLEM_QUERY = """
SELECT
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
FROM
    {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
WHERE
    verb_id in (
        'https://w3id.org/xapi/acrossx/verbs/evaluated',
        'http://adlnet.gov/expapi/verbs/passed',
        'http://adlnet.gov/expapi/verbs/asked'
    );
"""

NEW_PROBLEM_QUERY = """
SELECT
    event_id,
    emission_time,
    actor_id,
    object_id,
    splitByString('/', course_id)[-1] AS course_key,
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
FROM
    {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
WHERE
    verb_id in (
        'https://w3id.org/xapi/acrossx/verbs/evaluated',
        'http://adlnet.gov/expapi/verbs/passed',
        'http://adlnet.gov/expapi/verbs/asked'
    );
"""

OLD_NAVIGATION_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }} 
{on_cluster}
(
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
) ENGINE = {engine}
PRIMARY KEY (org, course_id, object_type)
ORDER BY (org, course_id, object_type, actor_id);
"""

NEW_NAVIGATION_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }} 
{on_cluster}
(
    `event_id` UUID NOT NULL,
    `emission_time` DateTime64(6) NOT NULL,
    `actor_id` String NOT NULL,
    `object_id` String NOT NULL,
    `course_key` String NOT NULL,
    `org` String NOT NULL,
    `verb_id` LowCardinality(String) NOT NULL,
    `object_type` LowCardinality(String) NOT NULL,
    `starting_position` Int16,
    `ending_point` String
) ENGINE = {engine}
PRIMARY KEY (org, course_key, object_type)
ORDER BY (org, course_key, object_type, actor_id);
"""

OLD_NAVIGATION_QUERY = """
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
"""

NEW_NAVIGATION_QUERY = """
SELECT
    event_id,
    emission_time,
    actor_id,
    object_id,
    splitByString('/', course_id)[-1] AS course_key,
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
"""

MIGRATIONS = [
    MvMigration(
        "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }}",
        OLD_ENROLLMENT_DDL,
        NEW_ENROLLMENT_DDL,
        "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_TRANSFORM_MV }}",
        OLD_ENROLLMENT_QUERY,
        NEW_ENROLLMENT_QUERY,
    ),
    MvMigration(
        "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}",
        OLD_VIDEO_DDL,
        NEW_VIDEO_DDL,
        "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_TRANSFORM_MV }}",
        OLD_VIDEO_QUERY,
        NEW_VIDEO_QUERY,
    ),
    MvMigration(
        "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }}",
        OLD_PROBLEM_DDL,
        NEW_PROBLEM_DDL,
        "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }}",
        OLD_PROBLEM_QUERY,
        NEW_PROBLEM_QUERY,
    ),
    MvMigration(
        "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }}",
        OLD_NAVIGATION_DDL,
        NEW_NAVIGATION_DDL,
        "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_TRANSFORM_MV }}",
        OLD_NAVIGATION_QUERY,
        NEW_NAVIGATION_QUERY,
    ),
]


def migrate(table_name, mv_name, table_ddl, mv_query):
    # for each table and materialized view to migrate:
    # - drop the existing table and materialized view if they exist
    # - create the new table
    # - load data into the new table using the new MV query
    # - create the materialized view using the new query
    op.execute(f"DROP TABLE IF EXISTS {table_name} {on_cluster}")
    op.execute(f"DROP VIEW IF EXISTS {mv_name} {on_cluster}")
    op.execute(table_ddl)
    op.execute(f"INSERT INTO {table_name} {mv_query}")
    mv_ddl = (
        f"CREATE MATERIALIZED VIEW IF NOT EXISTS {mv_name} {on_cluster} "
        f"TO {table_name} AS {mv_query}"
    )
    op.execute(mv_ddl)


def upgrade():
    for migration in MIGRATIONS:
        migrate(
            migration.table_name,
            migration.mv_name,
            migration.new_ddl,
            migration.new_mv_query,
        )


def downgrade():
    for migration in MIGRATIONS:
        migrate(
            migration.table_name,
            migration.mv_name,
            migration.old_ddl,
            migration.old_mv_query,
        )
