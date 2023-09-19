"""
create a top-level materialized view for grading events
"""
from alembic import op


revision = "0018"
down_revision = "0017"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_GRADING_EVENTS_TABLE }} 
        {on_cluster}
        (
            `event_id` UUID NOT NULL,
            `emission_time` DateTime64 NOT NULL,
            `actor_id` String NOT NULL,
            `object_id` String NOT NULL,
            `course_key` String NOT NULL,
            `org` String NOT NULL,
            `verb_id` LowCardinality(String) NOT NULL,
            `scaled_score` String
        ) ENGINE = {engine}
        PRIMARY KEY (org, course_key, verb_id)
        ORDER BY (org, course_key, verb_id, emission_time, actor_id, object_id, scaled_score, event_id);
        """
    )

    op.execute(
        f"""
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_GRADING_TRANSFORM_MV }}
        {on_cluster}
        TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_GRADING_EVENTS_TABLE }} AS
        SELECT
            event_id,
            cast(emission_time as DateTime) as emission_time,
            actor_id,
            object_id,
            splitByString('/', course_id)[-1] AS course_key,
            org,
            verb_id,
            JSON_VALUE(event_str, '$.result.score.scaled') as scaled_score
        FROM
            {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
        WHERE
            verb_id in (
                'http://id.tincanapi.com/verb/earned',
                'https://w3id.org/xapi/acrossx/verbs/evaluated'
            );
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_GRADING_EVENTS_TABLE }}"
        f"{on_cluster}"
    )
    op.execute(
        "DROP VIEW IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_GRADING_TRANSFORM_MV }}"
        f"{on_cluster}"
    )
