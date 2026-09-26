"""
Partition the event_sink.user_profile table

.. pii: Stores Open edX user profile data.
.. pii_types: user_id, name, username, location, phone_number, email_address, birth_date, biography, gender
.. pii_retirement: local_api, consumer_api
"""
from alembic import op


revision = "0027"
down_revision = "0026"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"

old_user_profile_table = "{{ASPECTS_EVENT_SINK_DATABASE}}.old_user_profile"

def upgrade():
    # Partition event_sink.user_profile table
    # 1. Rename old table
    op.execute(
        f"""
        RENAME TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
        TO {old_user_profile_table}
        {on_cluster}
        """
    )
    # 2. Create partitioned table from old data
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
        {on_cluster}
        (
            id Int32 NOT NULL,
            user_id Int32 NOT NULL,
            name String NOT NULL,
            meta String NOT NULL,
            courseware String NOT NULL,
            language String NOT NULL,
            location String NOT NULL,
            year_of_birth String NOT NULL,
            gender String NOT NULL,
            level_of_education String NOT NULL,
            mailing_address String NOT NULL,
            city String NOT NULL,
            country String NOT NULL,
            state String NOT NULL,
            goals String NOT NULL,
            bio String NOT NULL,
            profile_image_uploaded_at String NOT NULL,
            phone_number String NOT NULL,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) engine = {engine}
        PARTITION BY user_id MOD 100
        PRIMARY KEY (id, time_last_dumped)
        ORDER BY (id, time_last_dumped)
        """
    )
    # 3. Insert data from the old table into the new one
    op.execute(
        f"""
        INSERT INTO {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
        SELECT * FROM {old_user_profile_table}
        """
    )
    # 4. Drop the old table
    op.execute(
        f"""
        DROP TABLE {old_user_profile_table}
        {on_cluster}
        """
    )


def downgrade():
    # Un-partition the event_sink.user_profile table
    # 1a. Rename old table
    op.execute(
        f"""
        RENAME TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
        TO {old_user_profile_table}
        {on_cluster}
        """
    )

    # 2. Create un-partitioned table from old data
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
        {on_cluster}
        (
            id Int32 NOT NULL,
            user_id Int32 NOT NULL,
            name String NOT NULL,
            meta String NOT NULL,
            courseware String NOT NULL,
            language String NOT NULL,
            location String NOT NULL,
            year_of_birth String NOT NULL,
            gender String NOT NULL,
            level_of_education String NOT NULL,
            mailing_address String NOT NULL,
            city String NOT NULL,
            country String NOT NULL,
            state String NOT NULL,
            goals String NOT NULL,
            bio String NOT NULL,
            profile_image_uploaded_at String NOT NULL,
            phone_number String NOT NULL,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) engine = {engine}
        PRIMARY KEY (id, time_last_dumped)
        ORDER BY (id, time_last_dumped)
        """
    )
    # 3. Insert into new table from old one
    op.execute(
        f"""
        INSERT INTO {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
        SELECT * FROM {old_user_profile_table}
        """

    )
    # 4. Drop the old table
    op.execute(
        f"""
        DROP TABLE {old_user_profile_table}
        {on_cluster}
        """
    )
