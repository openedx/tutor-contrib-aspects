from alembic import op
import sqlalchemy as sa

revision = "0005"
down_revision = "0004"
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
        -- MV target table for problem interaction xAPI events
        CREATE TABLE IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }} (
            `event_id` UUID NOT NULL,
            `emission_time` DateTime64(6) NOT NULL,
            `actor_id` String NOT NULL,
            `object_id` String NOT NULL,
            `course_id` String NOT NULL,
            `org` String NOT NULL,
            `verb_id` LowCardinality(String) NOT NULL,
            `responses` String,
            `scaled_score` String,
            `success` Bool,
            `interaction_type` LowCardinality(String),
            `attempts` Int16
        ) ENGINE = MergeTree
        PRIMARY KEY (org, course_id, verb_id)
        ORDER BY (org, course_id, verb_id, actor_id);
        """
    )
    op.execute(
        """
        -- Materialized view that moves data from the processed xAPI table to
        -- the problem events table
        -- n.b. this query omits browser problem_checked events, as they do not
        -- contain any information that the server events don't have and including
        -- them would heavily skew the distribution of values in the problem
        -- response fields (responses, scaled_score, etc)
        CREATE MATERIALIZED VIEW IF NOT EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }}
            TO {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }} AS
        SELECT
            event_id,
            emission_time,
            actor_id,
            object_id,
            course_id,
            org,
            verb_id,
            JSON_VALUE(event_str, '$.result.response') as responses,
            JSON_VALUE(event_str, '$.result.score.scaled') as scaled_score,
            if(
                verb_id = 'https://w3id.org/xapi/acrossx/verbs/evaluated',
                cast(JSON_VALUE(event_str, '$.result.success') as Bool),
                false
            ) as success,
            JSON_VALUE(event_str, '$.object.definition.interactionType') as interaction_type,
            if(
                verb_id = 'https://w3id.org/xapi/acrossx/verbs/evaluated',
                cast(JSON_VALUE(event_str, '$.object.definition.extensions."http://id.tincanapi.com/extension/attempt-id"') as Int16),
                0
            ) as attempts
        FROM
            {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}
        WHERE
            verb_id in (
                'https://w3id.org/xapi/acrossx/verbs/evaluated',
                'http://adlnet.gov/expapi/verbs/passed',
                'http://adlnet.gov/expapi/verbs/asked'
            );
        """
    )


def downgrade():
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }};"
    )
    op.execute(
        "DROP TABLE IF EXISTS {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }};"
    )
