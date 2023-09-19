"""
create user_profile sink table
"""
from alembic import op


revision = "0016"
down_revision = "0015"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedReplacingMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "ReplacingMergeTree"


def upgrade():
    op.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_USER_PROFILE_TABLE }}
        {on_cluster}
        (
            id Int32 NOT NULL,
            user_id Int32 NOT NULL,
            name String NOT NULL,
            meta String NOT NULL,
            courseware String NOT NULL,
            language String NOT NULL,
            location String NOT NULL,
            year_of_birth String NOT NULL,
            gender String NOT NULL,
            level_of_education String NOT NULL,
            mailing_address String NOT NULL,
            city String NOT NULL,
            country String NOT NULL,
            state String NOT NULL,
            goals String NOT NULL,
            bio String NOT NULL,
            profile_image_uploaded_at String NOT NULL,
            phone_number String NOT NULL,
            dump_id UUID NOT NULL,
            time_last_dumped String NOT NULL
        ) engine = {engine}
        PRIMARY KEY (id, time_last_dumped)
        ORDER BY (id, time_last_dumped);
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_USER_PROFILE_TABLE }}"
        f"{on_cluster}"
    )
