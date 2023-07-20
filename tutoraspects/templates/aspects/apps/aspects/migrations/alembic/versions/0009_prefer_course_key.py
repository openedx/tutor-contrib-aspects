from alembic import op

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade():
    # n.b. we cann't rename the course_id column to course_key because it is used
    # as part of the primary key for the MV target tables
    op.execute("set allow_experimental_alter_materialized_view_structure=1;")
    op.execute(
        """
        ALTER TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_TRANSFORM_MV }}
        MODIFY QUERY
        SELECT
            event_id,
            emission_time,
            actor_id,
            object_id,
            splitByString('/', course_id)[-1] as course_id,
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

    op.execute(
        """
        ALTER TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_TRANSFORM_MV }}
        MODIFY QUERY
        SELECT
            event_id,
            emission_time,
            actor_id,
            object_id,
            splitByString('/', course_id)[-1] as course_id,
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

    op.execute(
        """
        ALTER TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }}
        MODIFY QUERY
        SELECT
            event_id,
            emission_time,
            actor_id,
            object_id,
            splitByString('/', course_id)[-1] as course_id,
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

    op.execute(
        """
        ALTER TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_TRANSFORM_MV }}
        MODIFY QUERY
        SELECT
            event_id,
            emission_time,
            actor_id,
            object_id,
            splitByString('/', course_id)[-1] as course_id,
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
    op.execute("set allow_experimental_alter_materialized_view_structure=1;")
    op.execute(
        """
        ALTER TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_TRANSFORM_MV }}
        MODIFY QUERY
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

    op.execute(
        """
        ALTER TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_TRANSFORM_MV }}
        MODIFY QUERY
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

    op.execute(
        """
        ALTER TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_TRANSFORM_MV }}
        MODIFY QUERY
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

    op.execute(
        """
        ALTER TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_TRANSFORM_MV }}
        MODIFY QUERY
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
