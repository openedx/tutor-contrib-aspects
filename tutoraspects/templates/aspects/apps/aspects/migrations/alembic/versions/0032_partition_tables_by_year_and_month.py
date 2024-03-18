"""
Partition the xapi table by year and month
"""
from alembic import op


revision = "0032"
down_revision = "0031"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"

old_xapi_table = "{{ASPECTS_XAPI_DATABASE}}.old_{{ASPECTS_RAW_XAPI_TABLE}}"

def upgrade():
    # Partition event_sink.user_profile table
    # 1. Rename old table
    op.execute(
        f"""
        RENAME TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        TO {old_xapi_table}
        {on_cluster}
        """
    )
    # 2. Create partitioned table from old data
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        {on_cluster}
        (
            event_id UUID NOT NULL,
            emission_time DateTime64(6) NOT NULL,
            event String NOT NULL
        ) ENGINE {engine}
        ORDER BY (emission_time, event_id)
        PARTITION BY toYYYYMM(emission_time)
        PRIMARY KEY (emission_time, event_id);
        """
    )
    # 3. Insert data from the old table into the new one
    op.execute(
        f"""
        INSERT INTO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        SELECT event_id, emission_time, event FROM {old_xapi_table}
        """
    )
    # 4. Drop the old table
    op.execute(
        f"""
        DROP TABLE {old_xapi_table}
        {on_cluster}
        """
    )


def downgrade():
    # Un-partition the event_sink.user_profile table
    # 1a. Rename old table
    op.execute(
        f"""
        RENAME TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        TO {old_xapi_table}
        {on_cluster}
        """
    )

    # 2. Create un-partitioned table from old data
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        {on_cluster}
        (
            event_id UUID NOT NULL,
            emission_time DateTime64(6) NOT NULL,
            event String NOT NULL
        ) ENGINE {engine}
        ORDER BY (emission_time, event_id)
        PRIMARY KEY (emission_time, event_id);
        """
    )
    # 3. Insert into new table from old one
    op.execute(
        f"""
        INSERT INTO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        SELECT * FROM {old_xapi_table}
        """

    )
    # 4. Drop the old table
    op.execute(
        f"""
        DROP TABLE {old_xapi_table}
        {on_cluster}
        """
    )
