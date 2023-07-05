from alembic import op
import sqlalchemy as sa

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        -- MV target table for navigation xAPI events
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }} (
            `event_id` UUID NOT NULL,
            `emission_time` DateTime64(6) NOT NULL,
            `actor_id` String NOT NULL,
            `object_id` String NOT NULL,
            `course_id` String NOT NULL,
            `org` String NOT NULL,
            `verb_id` LowCardinality(String) NOT NULL,
            `object_type` LowCardinality(String) NOT NULL,
            `starting_position` Int16,
            `ending_point` String
        ) ENGINE = MergeTree
        PRIMARY KEY (org, course_id, object_type)
        ORDER BY (org, course_id, object_type, actor_id);
        """
    )
    op.execute(
        """
        -- Materialized view that moves data from the processed xAPI table to
        -- the enrollment events table
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_TRANSFORM_MV }}
        TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }} AS
        SELECT
            event_id,
            emission_time,
            actor_id,
            object_id,
            course_id,
            org,
            verb_id,
            JSON_VALUE(event_str, '$.object.definition.type') AS object_type,
            -- clicking a link and selecting a module outline have no starting-position field
            if (
                object_type in (
                    'http://adlnet.gov/expapi/activities/link',
                    'http://adlnet.gov/expapi/activities/module'
                ),
                0,
                cast(JSON_VALUE(
                    event_str,
                    '$.context.extensions."http://id.tincanapi.com/extension/starting-position"'
                ) as Int16)
            ) AS starting_position,
            JSON_VALUE(
                event_str,
                '$.context.extensions."http://id.tincanapi.com/extension/ending-point"'
            ) AS ending_point
        FROM
            {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
        WHERE verb_id IN (
            'https://w3id.org/xapi/dod-isd/verbs/navigated'
        );
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }};"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_TRANSFORM_MV }};"
    )
