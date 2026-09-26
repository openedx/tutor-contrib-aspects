"""
create user_pii table sourced from an in-memory dictionary joining the PII tables.

This table is always created, but it will only be populated if ASPECTS_ENABLE_PII.
Once accessed, data from this dictionary is cached in-memory for ASPECTS_PII_CACHE_LIFETIME seconds.

.. pii: Stores Open edX user and profile data in a dictionary for use by Superset charts.
.. pii_types: user_id, name, username, location, phone_number, email_address, birth_date, biography, gender
.. pii_retirement: local_api, consumer_api
"""
from alembic import op


revision = "0028"
down_revision = "0027"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"

def upgrade():

    # We include these drop statements here because "CREATE OR REPLACE DICTIONARY"
    # currently throws a file rename error and you can't drop a dictionary with a
    # table referring to it.
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


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii"
        f"{on_cluster}"
    )
    op.execute(
        "DROP DICTIONARY IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii_dict"
        f"{on_cluster}"
    )
