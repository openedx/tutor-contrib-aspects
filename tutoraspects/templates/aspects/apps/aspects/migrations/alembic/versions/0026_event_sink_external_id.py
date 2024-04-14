"""
create external_id sink table

This table is always created, but it will only be populated if ASPECTS_ENABLE_PII.

.. pii: Stores a mapping between an Open edX user and their external_id values stored in Open edX.
.. pii_types: user_id, username
.. pii_retirement: local_api, consumer_api
"""
from alembic import op


revision = "0026"
down_revision = "0023"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.external_id
        {on_cluster}
        (
            `external_user_id` UUID NOT NULL,
            `external_id_type` String,
            `username` String,
            `user_id` Int32,
            `dump_id` UUID NOT NULL,
            `time_last_dumped` String NOT NULL
        )
        ENGINE = {engine}
        PRIMARY KEY (external_user_id, time_last_dumped)
        PARTITION BY user_id MOD 100
        ORDER BY (external_user_id, time_last_dumped)
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.external_id"
        f"{on_cluster}"
    )
