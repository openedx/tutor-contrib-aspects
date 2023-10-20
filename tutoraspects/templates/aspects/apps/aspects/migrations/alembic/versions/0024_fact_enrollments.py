"""
create a materialized view to populate a denormalized fact table of enrollment events
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
engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"


def upgrade():
    op.execute(
        f"""
        create table if not exists {{ ASPECTS_XAPI_DATABASE }}.fact_enrollments (
            emission_time DateTime,
            org String,
            course_key String,
            course_name String,
            course_run String,
            actor_id String,
            enrollment_mode LowCardinality(String),
            enrollment_status LowCardinality(String)
        ) ENGINE = {engine}
        PRIMARY KEY (org, course_key)
        ORDER BY (org, course_key, actor_id, enrollment_mode, enrollment_status, emission_time)
        """
    )

    op.execute(
        f"""
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.fact_enrollments_mv
        {on_cluster}
        TO {{ ASPECTS_XAPI_DATABASE }}.fact_enrollments AS
        select
            enrollments.emission_time as emission_time,
            enrollments.org as org,
            enrollments.course_key as course_key,
            courses.course_name as course_name,
            courses.course_run as course_run,
            enrollments.actor_id as actor_id,
            enrollments.enrollment_mode as enrollment_mode,
            splitByString('/', enrollments.verb_id)[-1] as enrollment_status
        from
            {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }} enrollments
            join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
                on enrollments.course_key = courses.course_key
        """
    )

    op.execute(
        """
        insert into {{ ASPECTS_XAPI_DATABASE }}.fact_enrollments
        select
            enrollments.emission_time as emission_time,
            enrollments.org as org,
            enrollments.course_key as course_key,
            courses.course_name as course_name,
            courses.course_run as course_run,
            enrollments.actor_id as actor_id,
            enrollments.enrollment_mode as enrollment_mode,
            splitByString('/', enrollments.verb_id)[-1] as enrollment_status
        from
            {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }} enrollments
            join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
                on enrollments.course_key = courses.course_key
    """
    )


def downgrade():
    op.execute("DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.fact_enrollments")
    op.execute("DROP VIEW IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.fact_enrollments_mv")
