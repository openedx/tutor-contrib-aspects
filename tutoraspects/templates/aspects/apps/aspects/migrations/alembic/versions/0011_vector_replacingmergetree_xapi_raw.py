from alembic import op


revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None

DESTINATION_TABLE = "{{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_XAPI_TABLE }}"
TMP_TABLE_NEW = f"{DESTINATION_TABLE}_tmp_{revision}"
TMP_TABLE_ORIG = f"{DESTINATION_TABLE}_tmp_mergetree_{revision}"
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
old_engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


def upgrade():
    # 1. Create our new table with the desired engine
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {TMP_TABLE_NEW}
        {on_cluster}
        (
            event_id      UUID,
            emission_time DateTime64(6),
            event_str     String
        )
        engine = {engine}
        PRIMARY KEY (emission_time)
        ORDER BY (emission_time, event_id);
        """
    )
    # 2. Attach our table to the existing partitions of the old MergeTree table.
    #    This works because our "order by" is the same. It should be instant no matter
    #    the size of the table since it's not copying anything.
    op.execute(
        f"""
        ALTER TABLE {TMP_TABLE_NEW}
        {on_cluster}
        ATTACH PARTITION tuple() FROM 
        {DESTINATION_TABLE};
        """
    )
    # 3. Swap both tables. We can't do this in a single statement because CH Cloud
    #    uses replicated tables and will error.
    op.execute(
        f"RENAME TABLE {DESTINATION_TABLE} TO {TMP_TABLE_ORIG} {on_cluster}"
    )
    op.execute(
        f"RENAME TABLE {TMP_TABLE_NEW} TO {DESTINATION_TABLE} {on_cluster}"
    )
    # 4. Force deduplication of the existing data and may take a very long time
    #    on a larger dataset, but since Aspects isn't in production anywhere yet this
    #    seems like a reasonable thing to do. If you're looking at this as fodder for
    #    a future migration, make sure to understand the potential issues here.
    op.execute(
        f"""
        OPTIMIZE TABLE {DESTINATION_TABLE} FINAL;
        """
    )
    # 5. Drop the renamed version of the original table.
    op.execute(
        f"""
        DROP TABLE {TMP_TABLE_ORIG} {on_cluster}
        """
    )


def downgrade():
    # 1. Create a new table with the old engine
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TMP_TABLE_ORIG}
        {on_cluster}
        (
            event_id      UUID,
            emission_time DateTime64(6),
            event_str     String
        )
        engine = {old_engine}
        PRIMARY KEY (emission_time)
        ORDER BY (emission_time, event_id);
        """
    )
    # 2. Attach our table to the existing partitions of the ReplacingMergeTree table.
    #    This works because our "order by" is the same. It should be instant no matter
    #    the size of the table since it's not copying anything.
    op.execute(
        f"""
        ALTER TABLE {TMP_TABLE_ORIG}
        {on_cluster}
        ATTACH PARTITION tuple() FROM 
        {DESTINATION_TABLE};
        """
    )
    # 3. Swap both tables. We can't do this in a single statement because CH Cloud
    #    uses replicated tables and will error.
    op.execute(f"RENAME TABLE {DESTINATION_TABLE} TO {TMP_TABLE_NEW} {on_cluster}")
    op.execute(f"RENAME TABLE {TMP_TABLE_ORIG} TO {DESTINATION_TABLE} {on_cluster}")

    # 4. Force deduplication of the existing data and may take a very long time
    #    on a larger dataset, but since Aspects isn't in production anywhere yet this
    #    seems like a reasonable thing to do. If you're looking at this as fodder for
    #    a future migration, make sure to understand the potential issues here.
    op.execute(
        f"""
        OPTIMIZE TABLE {DESTINATION_TABLE} 
        {on_cluster}
        FINAL DEDUPLICATE;
        """
    )
    # 5. Drop the renamed version of the original table.
    op.execute(
        f"""
        DROP TABLE {TMP_TABLE_NEW} {on_cluster}
        """
    )
