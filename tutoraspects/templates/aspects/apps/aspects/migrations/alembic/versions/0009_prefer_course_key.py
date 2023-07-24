from alembic import op

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


TABLES = {
    "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }}": """
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
        """,
    "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}": """
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
        """,
    "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }}": """
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
        """,
    "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }}": """
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
        """,
}


MATERIALIZED_VIEWS = {
    "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_TRANSFORM_MV }}": """
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
        """,
    "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_TRANSFORM_MV }}": """
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
        """,
    "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }}": """
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }}
            TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }} AS
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
        """,
    "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_TRANSFORM_MV }}": """
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
        """,
}


def upgrade():
    # drop the tables and MVs and create new ones, with course_id
    # replaced by course_key
    for name, ddl in TABLES.items():
        op.execute(f"DROP TABLE IF EXISTS {name}")
        op.execute(ddl.replace("course_id", "course_key"))

    for name, query in MATERIALIZED_VIEWS.items():
        op.execute(f"DROP TABLE {name}")
        op.execute(
            query.replace(
                "course_id", "splitByString('/', course_id)[-1] AS course_key"
            )
        )


def downgrade():
    for name, ddl in TABLES.items():
        op.execute(f"DROP TABLE IF EXISTS {name}")
        op.execute(ddl)

    for name, query in MATERIALIZED_VIEWS.items():
        op.execute(f"DROP TABLE IF EXISTS {name}")
        op.execute(query)
