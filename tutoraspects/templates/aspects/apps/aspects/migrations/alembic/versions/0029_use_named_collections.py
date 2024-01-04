"""
Update all existing dictionaries to use named collections.

In Jan 2024 we updated old Alembic migrations to use these, but any database
created before that will need these changes. This allowed us to get the
database credentials out of the migrations (and therefore not break everything
when changing the ClickHouse admin password). For databases created after 2024
these should change nothing.
"""

from alembic import op


revision = "0029"
down_revision = "0028"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


def upgrade():
    # We include these drop statements here because "CREATE OR REPLACE DICTIONARY"
    # currently throws a file rename error and you can't drop a dictionary with a
    # table referring to it.

    #######################
    # user_pii_dict changes
    op.execute(
        f"""
        DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii
        {on_cluster}
        """
    )
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii_dict
        {on_cluster}
        """
    )
    op.execute(
        f"""
        CREATE DICTIONARY {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii_dict
        {on_cluster}
        (
            user_id Int32,
            external_user_id UUID,
            external_id_type String,
            username String,
            name String,
            meta String,
            courseware String,
            language String,
            location String,
            year_of_birth String,
            gender String,
            level_of_education String,
            mailing_address String,
            city String,
            country String,
            state String,
            goals String,
            bio String,
            profile_image_uploaded_at String,
            phone_number String
        )
        PRIMARY KEY (user_id, external_user_id)
        SOURCE(CLICKHOUSE(
            name local_ch_event_sink
            query "
                with most_recent_user_profile as (
                    select
                        user_id,
                        name,
                        meta,
                        courseware,
                        language,
                        location,
                        year_of_birth,
                        gender,
                        level_of_education,
                        mailing_address,
                        city,
                        country,
                        state,
                        goals,
                        bio,
                        profile_image_uploaded_at,
                        phone_number,
                    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY (id, time_last_dumped) DESC) as rn
                    from {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_USER_PROFILE_TABLE }}
                )
                select
                    mrup.user_id as user_id,
                    external_user_id,
                    external_id_type,
                    username,
                    name,
                    meta,
                    courseware,
                    language,
                    location,
                    year_of_birth,
                    gender,
                    level_of_education,
                    mailing_address,
                    city,
                    country,
                    state,
                    goals,
                    bio,
                    profile_image_uploaded_at,
                    phone_number
                FROM {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_EXTERNAL_ID_TABLE }} ex
                RIGHT OUTER JOIN most_recent_user_profile mrup ON
                    mrup.user_id = ex.user_id and (
                       ex.external_id_type = 'xapi' OR
                       ex.external_id_type is NULL
                    )
                WHERE mrup.rn = 1
            "
        ))
        LAYOUT(COMPLEX_KEY_SPARSE_HASHED())
        LIFETIME({{ ASPECTS_PII_CACHE_LIFETIME }})
        """
    )
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii
        {on_cluster}
        (
            user_id Int32,
            external_user_id UUID,
            external_id_type String,
            username String,
            name String,
            meta String,
            courseware String,
            language String,
            location String,
            year_of_birth String,
            gender String,
            level_of_education String,
            mailing_address String,
            city String,
            country String,
            state String,
            goals String,
            bio String,
            profile_image_uploaded_at String,
            phone_number String
        ) engine = Dictionary({{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii_dict);
        """
    )

    # course_names_dict changes
    ###########################
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
            name local_ch_event_sink
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

    # course_block_names_dict changes
    ##################################
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
            name local_ch_event_sink
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
    """
    We can't downgrade these without adding the credentials back, so right now
    we do nothing. Earlier migrations will drop these as appropriate.
    """
    pass
