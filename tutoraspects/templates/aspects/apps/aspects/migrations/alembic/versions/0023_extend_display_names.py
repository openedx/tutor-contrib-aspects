from alembic import op

revision = "0023"
down_revision = "0022"
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


def drop_objects():
    op.execute(
        f"""
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_RECENT_BLOCKS_TABLE }}
        {on_cluster}
        """
    )

    op.execute(
        f"""
        DROP VIEW IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_RECENT_BLOCKS_MV }}
        {on_cluster}
        """
    )

    # We include these drop statements here because "CREATE OR REPLACE DICTIONARY"
    # currently throws a file rename error and you can't drop a dictionary with a
    # table referring to it.
    op.execute(
        f"""
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
        {on_cluster}
        """
    )
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict
        {on_cluster}
        """
    )


def upgrade():
    drop_objects()

    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_RECENT_BLOCKS_TABLE }}
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
        create materialized view if not exists {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_RECENT_BLOCKS_MV }}
        {on_cluster}
        to {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_RECENT_BLOCKS_TABLE }} as
        select
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
        from {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
        """
    )

    op.execute(
        """
        insert into {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_RECENT_BLOCKS_TABLE }} (
            location, display_name, display_name_with_location, section, subsection, unit, graded, course_key, dump_id, time_last_dumped
        )
        select
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
        from {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }};
        """
    )

    op.execute(
        f"""
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String,
            graded Bool,
            display_name_with_location String
        )
        PRIMARY KEY location
        SOURCE(CLICKHOUSE(
            user '{{ CLICKHOUSE_ADMIN_USER }}'
            password '{{ CLICKHOUSE_ADMIN_PASSWORD }}'
            db '{{ ASPECTS_EVENT_SINK_DATABASE }}'
            query "
                select
                    location,
                    display_name,
                    course_key,
                    graded,
                    display_name_with_location
                from {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_RECENT_BLOCKS_TABLE }}
                final
            "
        ))
        LAYOUT(COMPLEX_KEY_SPARSE_HASHED())
        LIFETIME(120);
        """
    )

    op.execute(
        f"""
        CREATE OR REPLACE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String,
            graded Bool,
            display_name_with_location String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict)
        ;
        """
    )


def downgrade():
    drop_objects()
    op.execute(
        f"""
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String,
            graded Bool
        )
        PRIMARY KEY location
        SOURCE(CLICKHOUSE(
            user '{{ CLICKHOUSE_ADMIN_USER }}'
            password '{{ CLICKHOUSE_ADMIN_PASSWORD }}'
            db '{{ ASPECTS_EVENT_SINK_DATABASE }}'
            query "with most_recent_blocks as (
                    select org, course_key, location, max(edited_on) as last_modified
                    from {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
                    group by org, course_key, location
                )
                select
                    location,
                    display_name,
                    course_key,
                    JSONExtractBool(xblock_data_json, 'graded') as graded
                from {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }} co
                inner join most_recent_blocks mrb on
                    co.org = mrb.org and
                    co.course_key = mrb.course_key and
                    co.location = mrb.location and
                    co.edited_on = mrb.last_modified
            "
        ))
        LAYOUT(COMPLEX_KEY_SPARSE_HASHED())
        LIFETIME(120);
        """
    )

    op.execute(
        f"""
        CREATE OR REPLACE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String,
            graded Bool
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict)
        ;
        """
    )
