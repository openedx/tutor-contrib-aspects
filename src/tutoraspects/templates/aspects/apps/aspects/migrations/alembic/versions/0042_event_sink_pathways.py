from alembic import op
import sqlalchemy as sa

revision = "0042"
down_revision = "0041"
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
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.catalog_pathway
        {on_cluster}
        (
            id Int64 NOT NULL,
            org String NOT NULL,
            pathway_code String NOT NULL,
            title String NOT NULL,
            category_code String NOT NULL,
            category_title String NOT NULL,
            created String NOT NULL,
            modified String NOT NULL,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) ENGINE {engine}
        ORDER BY (id, time_last_dumped)
        PRIMARY KEY (id, time_last_dumped);
        """
    )

    # Keyed by the learner's xAPI actor_id, never user_id or username, so the
    # table holds no PII and is written whatever ASPECTS_ENABLE_PII says.
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.pathway_enrollment
        {on_cluster}
        (
            id Int64 NOT NULL,
            catalog_pathway_id Int64 NOT NULL,
            actor_id String NOT NULL,
            created String NOT NULL,
            modified String NOT NULL,
            is_active Bool NOT NULL,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) ENGINE {engine}
        ORDER BY (id, time_last_dumped)
        PRIMARY KEY (id, time_last_dumped);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.pathway_enrollment"
        f"{on_cluster};"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.catalog_pathway"
        f"{on_cluster};"
    )
