from alembic import op
import sqlalchemy as sa

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE }}
        {on_cluster}
        (
            `time` DateTime,
            `message` String
        )
        ENGINE {engine}
        ORDER BY time;
        """
    )
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_XAPI_TABLE }}
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


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_XAPI_TABLE }}"
        f"{on_cluster}"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE }}"
        f"{on_cluster}"
    )
