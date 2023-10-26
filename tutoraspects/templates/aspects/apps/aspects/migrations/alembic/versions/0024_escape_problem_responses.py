"""
replace double-quoted strings in problem responses
"""

from alembic import op

revision = "0024"
down_revision = "0023"
branch_labels = None
depends_on = None
on_cluster = (
    " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' "
    if "{{CLICKHOUSE_CLUSTER_NAME}}"
    else ""
)
engine = (
    "ReplicatedReplacingMergeTree"
    if "{{CLICKHOUSE_CLUSTER_NAME}}"
    else "ReplacingMergeTree"
)


TABLE_NAME = "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }}"
VIEW_NAME = "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }}"

PROBLEM_DDL = f"""
CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }}
{on_cluster}
(
    `event_id` UUID NOT NULL,
    `emission_time` DateTime NOT NULL,
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
ORDER BY (org, course_key, verb_id, emission_time, actor_id, object_id, responses, success, event_id);
"""


OLD_PROBLEM_QUERY = """
SELECT
    event_id,
    cast(emission_time as DateTime) as emission_time,
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


NEW_PROBLEM_QUERY = """
SELECT
    event_id,
    cast(emission_time as DateTime) as emission_time,
    actor_id,
    object_id,
    splitByString('/', course_id)[-1] AS course_key,
    org,
    verb_id,
    replaceAll(
        replaceAll(
            JSON_VALUE(event_str, '$.result.response'),
            '\\\'', '\\\\\\\''
         ), '"', '\\\'') as responses,
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


def drop_objects():
    op.execute(
        f"""
        DROP TABLE IF EXISTS {TABLE_NAME} {on_cluster}
        """
    )

    op.execute(
        f"""
        DROP VIEW IF EXISTS {VIEW_NAME} {on_cluster}
        """
    )


def upgrade():
    drop_objects()
    op.execute(PROBLEM_DDL)
    op.execute(f"INSERT INTO {TABLE_NAME} {NEW_PROBLEM_QUERY}")
    op.execute(
        f"""
        CREATE MATERIALIZED VIEW {VIEW_NAME} {on_cluster} TO {TABLE_NAME} AS {NEW_PROBLEM_QUERY}
        """
    )


def downgrade():
    drop_objects()
    op.execute(PROBLEM_DDL)
    op.execute(f"INSERT INTO {TABLE_NAME} {OLD_PROBLEM_QUERY}")
    op.execute(
        f"""
        CREATE MATERIALIZED VIEW {VIEW_NAME} {on_cluster} TO {TABLE_NAME} AS {OLD_PROBLEM_QUERY}
        """
    )
