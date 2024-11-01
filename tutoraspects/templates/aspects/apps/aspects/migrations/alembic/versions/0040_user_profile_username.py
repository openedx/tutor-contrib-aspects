from alembic import op
import sqlalchemy as sa

revision = "0040"
down_revision = "0039"
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
        ALTER TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
        {on_cluster}
        ADD COLUMN IF NOT EXISTS username String DEFAULT ''
        AFTER name;
        """
    )


def downgrade():
    op.execute(
        f"""
        ALTER TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.user_profile
        {on_cluster}
        DROP COLUMN IF EXISTS username;
        """
    )
