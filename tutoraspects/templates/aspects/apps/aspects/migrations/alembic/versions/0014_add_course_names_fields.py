"""
add additional fields to course_names_dict and and course_names
"""
from alembic import op


revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""


def upgrade():
    # We include these drop statements here because "CREATE OR REPLACE DICTIONARY"
    # currently throws a file rename error and you can't drop a dictionary with a
    # table referring to it.
    op.execute(
        f"""
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names 
        {on_cluster}
        """
    )
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict
        {on_cluster} 
        """
    )

    op.execute(
        f"""
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict 
        {on_cluster}
        (
            course_key String,
            course_name String,
            course_run String,
            org String
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
                display_name,
                splitByString(\\'+\\', course_key)[-1] as course_run,
                org
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
        CREATE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names
        {on_cluster}
        (
            course_key String,
            course_name String,
            course_run String,
            org String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict);
        """
    )


def downgrade():
    op.execute(
        f"""
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names
        {on_cluster}
        """
    )
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict
        {on_cluster}
        """
    )

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
        CREATE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names
        {on_cluster}
        (
            course_key String,
            course_name String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict);
        """
    )
