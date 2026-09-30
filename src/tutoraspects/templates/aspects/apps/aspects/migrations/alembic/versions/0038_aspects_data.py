from alembic import op
import sqlalchemy as sa

revision = "0038"
down_revision = "0037"
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
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.aspects_data
        {on_cluster}
        (
            path String NOT NULL,
            content String NOT NULL,
        ) ENGINE {engine}
        PRIMARY KEY (path);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.aspects_data"
        f"{on_cluster};"
    )
