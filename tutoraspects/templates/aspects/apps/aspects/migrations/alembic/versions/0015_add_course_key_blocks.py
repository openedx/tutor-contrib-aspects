"""
add additional fields to course_block_names_dict and course_block_names
"""
from alembic import op


revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def drop_objects():
    # We include these drop statements here because "CREATE OR REPLACE DICTIONARY"
    # currently throws a file rename error and you can't drop a dictionary with a
    # table referring to it.
    op.execute(
        """
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names;
    """
    )
    op.execute(
        """
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict;
    """
    )


def upgrade():
    drop_objects()
    op.execute(
        """
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict (
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
        """
        CREATE OR REPLACE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
        (
            location String,
            block_name String,
            course_key String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict)
        ;
        """
    )


def downgrade():
    drop_objects()
    op.execute(
        """
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict (
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
        """
        CREATE OR REPLACE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
        (
            location String,
            block_name String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names_dict)
        ;
        """
    )
