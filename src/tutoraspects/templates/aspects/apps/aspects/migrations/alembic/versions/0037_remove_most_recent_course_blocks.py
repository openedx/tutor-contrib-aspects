"""
This MV should have been moved to dbt, but was missed in the migration and existed
in a weird, unused state from 0035 until this migration.
"""

from alembic import op


revision = "0037"
down_revision = "0036"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = (
    "ReplicatedReplacingMergeTree"
    if "{{CLICKHOUSE_CLUSTER_NAME}}"
    else "ReplacingMergeTree"
)


def drop_objects():
    """
    Since alembic and dbt both need these to be removed to ensure the correct new
    version gets created, we share the drop code here.
    """
    op.execute(
        f"""
        DROP VIEW IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks_mv
        {on_cluster}
        """
    )

    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
        {on_cluster}
        """
    )

    op.execute(
        f"""
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks
        {on_cluster}
        """
    )


def upgrade():
    drop_objects()


def downgrade():
    drop_objects()

    op.execute(
        f"""
        CREATE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks
        {on_cluster}
        (
            location String NOT NULL,
            display_name String NOT NULL,
            display_name_with_location String NOT NULL,
            section Int32,
            subsection Int32,
            unit Int32,
            graded Bool,
            course_key String,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) engine = {engine}
            PRIMARY KEY (location);
        """
    )

    op.execute(
        f"""
        CREATE MATERIALIZED VIEW {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks_mv
        {on_cluster}
        TO {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks as
        SELECT
            location,
            display_name,
            toString(section) || ':' || toString(subsection) || ':' || toString(unit) || ' - ' || display_name as display_name_with_location,
            JSONExtractInt(xblock_data_json, 'section') as section,
            JSONExtractInt(xblock_data_json, 'subsection') as subsection,
            JSONExtractInt(xblock_data_json, 'unit') as unit,
            JSONExtractBool(xblock_data_json, 'graded') as graded,
            course_key,
            dump_id,
            time_last_dumped
        FROM {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks
        """
    )

    op.execute(
        """
        INSERT INTO {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks (
            location, display_name, display_name_with_location, section, subsection, unit, graded, course_key, dump_id, time_last_dumped
        )
        SELECT
            location,
            display_name,
            toString(section) || ':' || toString(subsection) || ':' || toString(unit) || '- ' || display_name as display_name_with_location,
            JSONExtractInt(xblock_data_json, 'section') as section,
            JSONExtractInt(xblock_data_json, 'subsection') as subsection,
            JSONExtractInt(xblock_data_json, 'unit') as unit,
            JSONExtractBool(xblock_data_json, 'graded') as graded,
            course_key,
            dump_id,
            time_last_dumped
        FROM {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks
        """
    )
