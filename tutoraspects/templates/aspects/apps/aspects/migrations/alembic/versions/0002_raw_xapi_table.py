from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"


def upgrade():
    op.execute(
        """
        SET allow_experimental_object_type=1;
        """
    )
    op.execute(
        f"""
        -- Raw table that Ralph writes to
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        {on_cluster} 
        (      
            event_id UUID NOT NULL,
            emission_time DateTime64(6) NOT NULL,
            event JSON NOT NULL,
            event_str String NOT NULL
        ) ENGINE {engine}
        ORDER BY (emission_time, event_id)
        PRIMARY KEY (emission_time, event_id);
        """
    )
    op.execute(
        f"""
        -- Processed table that Superset reads from
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }} 
        {on_cluster}
        (
            event_id UUID NOT NULL,
            verb_id String NOT NULL,
            actor_id String NOT NULL,
            object_id String NOT NULL,
            org String NOT NULL,
            course_id String NOT NULL,
            emission_time DateTime64(6) NOT NULL,
            event_str String NOT NULL
        ) ENGINE {engine}
        ORDER BY (org, course_id, verb_id, actor_id, emission_time, event_id)
        PRIMARY KEY (org, course_id, verb_id, actor_id, emission_time, event_id);
        """
    )
    op.execute(
        f"""
        -- Materialized view that moves data from the raw table to processed table
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TRANSFORM_MV }}
        {on_cluster}
        TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }} 
        AS
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
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}"
        f"{on_cluster};"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}"
        f"{on_cluster};"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TRANSFORM_MV }}"
        f"{on_cluster}"
    )
