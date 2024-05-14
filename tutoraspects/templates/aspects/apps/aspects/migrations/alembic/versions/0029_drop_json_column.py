"""
As part of the Ralph 4.0 upgrade, we drop the unused JSON column "event"
and rename "event_json" to "event".
"""
from alembic import op


revision = "0029"
down_revision = "0028"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"

# Only used in downgrade, where we have to move data
upgraded_table_name = "{{ASPECTS_XAPI_DATABASE}}.old_{{ASPECTS_RAW_XAPI_TABLE}}"


def upgrade():
    op.execute(
        f"""
        DROP VIEW IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.xapi_events_all_parsed_mv;
        """
    )
    op.execute(
        f"""
        ALTER TABLE  {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }} 
        {on_cluster} 
        DROP COLUMN event, RENAME COLUMN event_str to event;
        """
    )


def downgrade():
    # 0. Remove the MV that may be pointing at the table we're changing
    op.execute(
        f"""
        DROP VIEW IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.xapi_events_all_parsed_mv;
        """
    )
    # 1. Rename updated table
    op.execute(
        f"""
        RENAME TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        TO {upgraded_table_name}
        {on_cluster}
        """
    )
    # 2. Create downgraded table, this is necessary because there are known
    #    issues with adding JSON columns to existing tables, and some versions
    #    of ClickHouse will error if you try.
    op.execute(
        f"""
        -- Raw table that Ralph writes to
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        {on_cluster} 
        (      
            event_id UUID NOT NULL,
            emission_time DateTime64(6) NOT NULL,
            event String NOT NULL,
            event_str String NOT NULL
        ) ENGINE {engine}
        ORDER BY (emission_time, event_id)
        PRIMARY KEY (emission_time, event_id);
        """
    )
    # 3. Insert data from the old table into the new one
    op.execute(
        f"""
        INSERT INTO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }}
        (event_id, emission_time, event, event_str)
        SELECT event_id, emission_time, event, event as event_str 
        FROM {upgraded_table_name}
        """
    )
    # 4. Drop the old table
    op.execute(
        f"""
        DROP TABLE {upgraded_table_name}
        {on_cluster}
        """
    )
