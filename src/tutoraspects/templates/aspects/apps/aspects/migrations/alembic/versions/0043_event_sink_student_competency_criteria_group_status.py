from alembic import op

revision = "0043"
down_revision = "0042"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = (
    "ReplicatedReplacingMergeTree"
    if "{{CLICKHOUSE_CLUSTER_NAME}}"
    else "ReplacingMergeTree"
)


def upgrade():
    # A learner's current mastery status for one competency criteria group
    # (openedx-core StudentCompetencyCriteriaGroupStatus): the only place
    # AttemptedNotDemonstrated is stored, and, for course-level groups, the
    # learner's status in one course. The group's competency, course and level
    # are denormalized so no criteria-group table is needed. Keyed by the
    # learner's xAPI actor_id, never user_id or username, so the table holds no
    # PII and is written whatever ASPECTS_ENABLE_PII says.
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.student_competency_criteria_group_status
        {on_cluster}
        (
            id Int64 NOT NULL,
            actor_id String NOT NULL,
            group_id Int64 NOT NULL,
            parent_group_id Nullable(Int64),
            tag_id Int64 NOT NULL,
            taxonomy_id Int64 NOT NULL,
            course_key String NOT NULL,
            group_level LowCardinality(String) NOT NULL,
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
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.student_competency_criteria_group_status"
        f"{on_cluster};"
    )
