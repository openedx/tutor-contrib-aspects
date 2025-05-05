select
    last_response.emission_time as emission_time,
    last_response.org as org,
    last_response.course_key as course_key,
    blocks.course_name as course_name,
    blocks.course_run as course_run,
    last_response.problem_id as problem_id,
    blocks.block_name as problem_name,
    blocks.display_name_with_location as problem_name_with_location,
    blocks.course_order as course_order,
    concat(
        '<a href="',
        last_response.object_id,
        '" target="_blank">',
        problem_name_with_location,
        '</a>'
    ) as problem_link,
    last_response.actor_id as actor_id,
    last_response.responses as responses,
    last_response.success as success,
    last_response.attempt as attempts,
    last_response.interaction_type as interaction_type,
    blocks.graded as graded,
    users.username as username,
    users.email as email,
    users.name as name
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_response as last_response
join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
    on (
        last_response.course_key = blocks.course_key
        and last_response.problem_id = blocks.block_id
    )
left outer join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii users
    on (
        last_response.actor_id like 'mailto:%'
        and SUBSTRING(last_response.actor_id, 8) = users.email
    )
    or last_response.actor_id = toString(users.external_user_id)

where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
