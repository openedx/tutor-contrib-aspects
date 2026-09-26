"""
add a 'graded' boolean to course_block_names_dict and course_block_names
"""
from alembic import op


revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""


def drop_objects():
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
                    from {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks
                    group by org, course_key, location
                )
                select
                    location,
                    display_name,
                    course_key,
                    JSONExtractBool(xblock_data_json, 'graded') as graded
                from {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks co
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


def downgrade():
    drop_objects()
    op.execute(
        f"""
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict 
        {on_cluster}
        (
            location String,
            block_name String,
            course_key String
        )
        PRIMARY KEY location
        SOURCE(CLICKHOUSE(
            user '{{ CLICKHOUSE_ADMIN_USER }}'
            password '{{ CLICKHOUSE_ADMIN_PASSWORD }}'
            db '{{ ASPECTS_EVENT_SINK_DATABASE }}'
            query 'with most_recent_blocks as (
                    select org, course_key, location, max(edited_on) as last_modified
                    from {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks
                    group by org, course_key, location
                )
                select
                    location,
                    display_name,
                    course_key
                from {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks co
                inner join most_recent_blocks mrb on
                    co.org = mrb.org and
                    co.course_key = mrb.course_key and
                    co.location = mrb.location and
                    co.edited_on = mrb.last_modified
            '
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
            course_key String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict)
        ;
        """
    )
