from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        SET allow_experimental_object_type=1;
        """
    )
    op.execute(
        """
        -- MV target table for enrollment xAPI events
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }} (
            `event_id` UUID NOT NULL,
            `emission_time` DateTime64(6) NOT NULL,
            `actor_id` String NOT NULL,
            `object_id` String NOT NULL,
            `course_id` String NOT NULL,
            `org` String NOT NULL,
            `verb_id` LowCardinality(String) NOT NULL,
            `enrollment_mode` LowCardinality(String)
        ) ENGINE = MergeTree
        PRIMARY KEY (org, course_id)
        ORDER BY (org, course_id, actor_id, enrollment_mode, emission_time);
        """
    )
    op.execute(
        """
        -- Processed table that Superset reads from
        -- Materialized view that moves data from the processed xAPI table to
        -- the enrollment events table
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_TRANSFORM_MV }}
            TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }} AS
        SELECT
            event_id,
            emission_time,
            actor_id,
            object_id,
            course_id,
            org,
            verb_id,
            JSON_VALUE(event_str, '$.object.definition.extensions."https://w3id.org/xapi/acrossx/extensions/type"') AS enrollment_mode
        FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
        WHERE verb_id IN (
            'http://adlnet.gov/expapi/verbs/registered',
            'http://id.tincanapi.com/verb/unregistered'
        );
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }};"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_TRANSFORM_MV }};"
    )
