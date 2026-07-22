"""
Create the load_test_stats table

This table is always created, but it will only be populated if the load test
management commands are run from the platform_plugin_aspects app.
"""
from alembic import op


revision = "0034"
down_revision = "0033"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.load_test_runs
        {on_cluster}
        (
            run_id     String,
            timestamp  DateTime default now(),
            event_type String,
            extra      String
        )
        engine = {engine} PRIMARY KEY (run_id, timestamp)
        ORDER BY (run_id, timestamp)
        SETTINGS index_granularity = 8192;
        """
    )

    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.load_test_stats
        {on_cluster}
        (
            run_id    String,
            timestamp DateTime default now(),
            stats     String
        )
        engine = {engine} PRIMARY KEY (run_id, timestamp)
        ORDER BY (run_id, timestamp)
        SETTINGS index_granularity = 8192;
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.load_test_stats"
        f"{on_cluster}"
    )

    op.execute(
        "DROP TABLE IF EXISTS {{ASPECTS_EVENT_SINK_DATABASE}}.load_test_runs"
        f"{on_cluster}"
    )
