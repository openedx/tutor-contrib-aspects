from alembic import op
import sqlalchemy as sa

revision = "0007"
down_revision = "0002"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_overviews
        {on_cluster}
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
        ) engine = {engine}
            PRIMARY KEY (org, course_key, modified, time_last_dumped)
            ORDER BY (org, course_key, modified, time_last_dumped);
        """
    )
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks
        {on_cluster}
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
        ) engine = {engine}
            PRIMARY KEY (org, course_key, location, edited_on)
            ORDER BY (org, course_key, location, edited_on, order);
        """
    )
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_relationships
        {on_cluster}
        (
            course_key String NOT NULL,
            parent_location String NOT NULL,
            child_location String NOT NULL,
            order Int32 NOT NULL,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) engine = {engine}
            PRIMARY KEY (course_key, parent_location, child_location, time_last_dumped)
            ORDER BY (course_key, parent_location, child_location, time_last_dumped, order);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_relationships"
        f"{on_cluster}"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks"
        f"{on_cluster}"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_overviews"
        f"{on_cluster}"
    )
