from alembic import op

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
    # A learner's current mastery status for one competency (openedx-core
    # StudentCompetencyStatus). Keyed by the learner's xAPI actor_id, never
    # user_id or username, so the table holds no PII and is written whatever
    # ASPECTS_ENABLE_PII says. Statuses only rise, so every dump is a newer
    # version of the same row.
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.student_competency_status
        {on_cluster}
        (
            id Int64 NOT NULL,
            actor_id String NOT NULL,
            tag_id Int64 NOT NULL,
            taxonomy_id Int64 NOT NULL,
            status_id UInt8 NOT NULL,
            status String NOT NULL,
            created String NOT NULL,
            modified String NOT NULL,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) ENGINE {engine}
        ORDER BY (id, time_last_dumped)
        PRIMARY KEY (id, time_last_dumped);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.student_competency_status"
        f"{on_cluster};"
    )
