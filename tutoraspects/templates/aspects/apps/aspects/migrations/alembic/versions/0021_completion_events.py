"""
create a top-level materialized view for completion events
"""
from alembic import op


revision = "0021"
down_revision = "0020"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_COMPLETION_EVENTS_TABLE }} 
        {on_cluster}
        (
            `event_id` UUID NOT NULL,
            `emission_time` DateTime64 NOT NULL,
            `actor_id` String NOT NULL,
            `object_id` String NOT NULL,
            `course_key` String NOT NULL,
            `org` String NOT NULL,
            `verb_id` LowCardinality(String) NOT NULL,
            `progress_percent` Int32,
        ) ENGINE = {engine}
        PRIMARY KEY (org, course_key, verb_id)
        ORDER BY (org, course_key, verb_id, emission_time, actor_id, object_id, event_id);
        """
    )

    op.execute(
        f"""
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_COMPLETION_TRANSFORM_MV }}
        {on_cluster}
        TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_COMPLETION_EVENTS_TABLE }} AS
        SELECT
            event_id,
            cast(emission_time as DateTime) as emission_time,
            actor_id,
            object_id,
            splitByString('/', course_id)[-1] AS course_key,
            org,
            verb_id,
            JSON_VALUE(event_str, '$.result.extensions."https://w3id.org/xapi/cmi5/result/extensions/progress"') as progress_percent
        FROM
            {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
        WHERE
            verb_id = 'http://adlnet.gov/expapi/verbs/progressed';
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_COMPLETION_EVENTS_TABLE }}"
        f"{on_cluster}"
    )
    op.execute(
        "DROP VIEW IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_COMPLETION_TRANSFORM_MV }}"
        f"{on_cluster}"
    )
