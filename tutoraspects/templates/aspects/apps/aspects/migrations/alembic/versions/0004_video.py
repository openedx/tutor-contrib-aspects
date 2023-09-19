from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""
engine = "ReplicatedMergeTree" if "{{CLICKHOUSE_CLUSTER_NAME}}" else "MergeTree"


def upgrade():
    op.execute(
        """
        SET allow_experimental_object_type=1;
        """
    )
    op.execute(
        f"""
        -- MV target table for video playback xAPI events
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }} 
        {on_cluster}
        (
            `event_id` UUID NOT NULL,
            `emission_time` DateTime64(6) NOT NULL,
            `actor_id` String NOT NULL,
            `object_id` String NOT NULL,
            `course_id` String NOT NULL,
            `org` String NOT NULL,
            `verb_id` LowCardinality(String) NOT NULL,
            `video_position` Float32 NOT NULL
        ) ENGINE = {engine}
        PRIMARY KEY (org, course_id, verb_id)
        ORDER BY (org, course_id, verb_id, actor_id);
        """
    )
    op.execute(
        f"""
        -- Materialized view that moves data from the processed xAPI table to
        -- the video playback events table
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_TRANSFORM_MV }}
        {on_cluster}
        TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }} AS
        SELECT
            event_id,
            emission_time,
            actor_id,
            object_id,
            course_id,
            org,
            verb_id,
            cast(coalesce(
                nullif(JSON_VALUE(event_str, '$.result.extensions."https://w3id.org/xapi/video/extensions/time"'), ''),
                nullif(JSON_VALUE(event_str, '$.result.extensions."https://w3id.org/xapi/video/extensions/time-from"'), ''),
                '0.0'
            ) as Float32) as video_position
        FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
        WHERE verb_id IN (
            'http://adlnet.gov/expapi/verbs/completed',
            'http://adlnet.gov/expapi/verbs/initialized',
            'http://adlnet.gov/expapi/verbs/terminated',
            'https://w3id.org/xapi/video/verbs/paused',
            'https://w3id.org/xapi/video/verbs/played',
            'https://w3id.org/xapi/video/verbs/seeked'
        );
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}"
        f"{on_cluster}"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_TRANSFORM_MV }}"
        f"{on_cluster}"
    )
