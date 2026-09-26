from alembic import op
import sqlalchemy as sa

revision = "0036"
down_revision = "0035"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_enrollment
        {on_cluster}
        (
            id Int32 NOT NULL,
            course_key String NOT NULL,
            created String NOT NULL,
            is_active Bool NOT NULL,
            mode LowCardinality(String) NOT NULL,
            username String NOT NULL,
            user_id Int32 NOT NULL,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) ENGINE {engine}
        ORDER BY (course_key, user_id, time_last_dumped)
        PRIMARY KEY (course_key, user_id, time_last_dumped);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.course_enrollment"
        f"{on_cluster};"
    )
