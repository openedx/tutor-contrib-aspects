from alembic import op
import sqlalchemy as sa

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None

def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE }}
        (
            `time` DateTime,
            `message` String
        )
        ENGINE MergeTree
        ORDER BY time;
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_XAPI_TABLE }}
        (
            event_id      UUID,
            emission_time DateTime64(6),
            event_str     String
        )
        engine = MergeTree
        PRIMARY KEY (emission_time)
        ORDER BY (emission_time, event_id);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_XAPI_TABLE }};"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_VECTOR_DATABASE }}.{{ ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE }};"
    )
