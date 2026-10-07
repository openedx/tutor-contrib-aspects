"""
Migrate dictionaries to DBT.
"""
from alembic import op


revision = "0035"
down_revision = "0034"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = (
    "ReplicatedReplacingMergeTree"
    if "{{CLICKHOUSE_CLUSTER_NAME}}"
    else "ReplacingMergeTree"
)

def upgrade():
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii
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
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
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
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names
        {on_cluster}
        """
    )
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names_dict
        {on_cluster}
        """
    )





def downgrade():
    ## Course Names
    op.execute(
        f"""
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii
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
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names
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
        DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names
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

    ## Course Block Names
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks
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
        create materialized view if not exists {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks_mv
        {on_cluster}
        to {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks as
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
        from {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks
        """
    )

    op.execute(
        """
        insert into {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks (
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
        from {{ ASPECTS_EVENT_SINK_DATABASE }}.course_blocks;
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
                from {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_course_blocks
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

    ## User PII
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
            user '{{ CLICKHOUSE_ADMIN_USER }}'
            password '{{ CLICKHOUSE_ADMIN_PASSWORD }}'
            db '{{ ASPECTS_EVENT_SINK_DATABASE }}'
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
                    from {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
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
                FROM {{ ASPECTS_EVENT_SINK_DATABASE }}.external_id ex
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
