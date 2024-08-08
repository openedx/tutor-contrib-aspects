from alembic import op
import sqlalchemy as sa

revision = "0010"
down_revision = "0008"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


def upgrade():
    # We include these drop statements here because "CREATE OR REPLACE DICTIONARY"
    # currently throws a file rename error and you can't drop a dictionary with a
    # table referring to it.
    op.execute(f"""
        DETACH DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names
        {on_cluster}
    """)
    op.execute(f"""
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names 
        {on_cluster}
        SYNC
    """)
    op.execute(f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict
        {on_cluster}
        SYNC
    """)
    op.execute(f"""
        DETACH DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names 
        {on_cluster}
    """)
    op.execute(f"""
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
        {on_cluster}
        SYNC
    """)
    op.execute(f"""
        DROP DICTIONARY IF EXISTS
        {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict
        {on_cluster}
        SYNC
    """)
    op.execute(
        f"""
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict 
        {on_cluster}
        (
            course_key String,
            course_name String
        )
        PRIMARY KEY course_key
        SOURCE(CLICKHOUSE(
            user '{{ CLICKHOUSE_ADMIN_USER }}'
            password '{{ CLICKHOUSE_ADMIN_PASSWORD }}'
            db '{{ ASPECTS_EVENT_SINK_DATABASE }}'
            query 'with most_recent_overviews as (
                    select org, course_key, max(modified) as last_modified
                    from {{ ASPECTS_EVENT_SINK_DATABASE }}.course_overviews
                    group by org, course_key
            )
            select
                course_key,
                display_name
            from {{ ASPECTS_EVENT_SINK_DATABASE }}.course_overviews co
            inner join most_recent_overviews mro on
                co.org = mro.org and
                co.course_key = mro.course_key and
                co.modified = mro.last_modified
            '
        ))
        LAYOUT(COMPLEX_KEY_HASHED())
        LIFETIME(120);
        """
    )
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names
        {on_cluster}
        (
            course_key String,
            course_name String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict);
        """
    )
    op.execute(
        f"""
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict 
        {on_cluster}
        (
            location String,
            block_name String
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
                    display_name
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
            block_name String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict)
        ;
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names "
        f"{on_cluster}"
    )
    op.execute(
        "DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict "
        f"{on_cluster}"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names "
        f"{on_cluster}"
    )
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS 
        {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict
        {on_cluster}
        """
    )
