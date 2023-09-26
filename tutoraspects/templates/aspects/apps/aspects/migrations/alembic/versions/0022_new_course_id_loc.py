"""
Update xapi_events_all_parsed_mv to parse the course id from
new places due to changes in how multi-question problem_checks
are handled.
"""
from alembic import op

revision = "0022"
down_revision = "0021"
branch_labels = None
depends_on = None

DESTINATION_TABLE = "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}"
TMP_TABLE_NEW = f"{DESTINATION_TABLE}_tmp_{revision}"
TMP_TABLE_ORIG = f"{DESTINATION_TABLE}_tmp_mergetree_{revision}"
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
old_engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


def upgrade():
    op.execute(
        """
        SET allow_experimental_object_type=1;
        """
    )
    op.execute(
        # There is not currently a "CREATE OR REPLACE MATERIALIZED VIEW..."
        f"""
        DROP VIEW IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TRANSFORM_MV }}
        {on_cluster};
        """
    )
    op.execute(
        f"""
        -- Materialized view that moves data from the raw table to processed table
        CREATE MATERIALIZED VIEW {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TRANSFORM_MV }}
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
        -- If the contextActivities parent is a course, use that. It can be a "course" 
        -- type, or a "cmi.interaction" type for multiple question problem submissions. 
        -- Otherwise use the object id for the course id.
        multiIf(
            -- If the contextActivities parent is a course, use that
            JSON_VALUE(
                event_str,
                '$.context.contextActivities.parent[0].definition.type'
            ) = 'http://adlnet.gov/expapi/activities/course',
            JSON_VALUE(event_str, '$.context.contextActivities.parent[0].id'),
            -- Else if the contextActivities parent is a GroupActivity, it's a multi
            -- question problem and we use the grouping id 
            JSON_VALUE(
                event_str,
                '$.context.contextActivities.parent[0].objectType'
            ) in ('Activity', 'GroupActivity'),
            JSON_VALUE(event_str, '$.context.contextActivities.grouping[0].id'),
            -- Otherwise use the object id
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
        """
        SET allow_experimental_object_type=1;
        """
    )
    op.execute(
        # There is not currently a "CREATE OR REPLACE MATERIALIZED VIEW..."
        f"""
        DROP VIEW IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TRANSFORM_MV }}
        {on_cluster};
        """
    )
    op.execute(
        f"""
        -- Materialized view that moves data from the raw table to processed table
        CREATE MATERIALIZED VIEW {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TRANSFORM_MV }}
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
