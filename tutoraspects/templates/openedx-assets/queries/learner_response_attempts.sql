-- select one record per (learner, problem, course, org) tuple
-- contains either the first successful attempt
-- or the most recent unsuccessful attempt
-- find the timestamp of the earliest successful response
-- this will be used to pick the xAPI event corresponding to that submission
with
    successful_responses as (
        select
            org, course_key, problem_id, actor_id::String as actor_id, first_success_at
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_response_attempt
        where
            isNotNull(first_success_at)
            {% include 'openedx-assets/queries/common_filters.sql' %}
    ),
    -- for all learners who did not submit a successful response,
    -- find the timestamp of the most recent unsuccessful response
    unsuccessful_responses as (
        select
            org,
            course_key,
            problem_id,
            actor_id::String as actor_id,
            max(last_attempt_at) as last_attempt_at
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_response_attempt
        where
            actor_id not in (select distinct actor_id from successful_responses)
            {% include 'openedx-assets/queries/common_filters.sql' %}
        group by org, course_key, problem_id, actor_id
    ),
    -- combine result sets for successful and unsuccessful problem submissions
    responses as (
        select org, course_key, problem_id, actor_id, first_success_at as emission_time
        from successful_responses
        union all
        select org, course_key, problem_id, actor_id, last_attempt_at as emission_time
        from unsuccessful_responses
    ),
    full_responses as (
        select
            events.emission_time as emission_time,
            events.org as org,
            events.course_key as course_key,
            events.problem_id as problem_id,
            events.object_id as object_id,
            events.actor_id as actor_id,
            events.responses as responses,
            events.success as success,
            events.attempts as attempts,
            events.interaction_type as interaction_type
        from {{ ASPECTS_XAPI_DATABASE }}.problem_events events
        join responses using (org, course_key, problem_id, actor_id, emission_time)
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    )

select
    full_responses.emission_time as emission_time,
    full_responses.org as org,
    full_responses.course_key as course_key,
    blocks.course_name as course_name,
    blocks.course_run as course_run,
    full_responses.problem_id as problem_id,
    blocks.block_name as problem_name,
    blocks.display_name_with_location as problem_name_with_location,
    blocks.course_order as course_order,
    concat(
        '<a href="',
        full_responses.object_id,
        '" target="_blank">',
        problem_name_with_location,
        '</a>'
    ) as problem_link,
    full_responses.actor_id as actor_id,
    full_responses.responses as responses,
    full_responses.success as success,
    full_responses.attempts as attempts,
    full_responses.interaction_type as interaction_type,
    blocks.graded as graded,
    users.username as username,
    users.email as email,
    users.name as name
from full_responses
join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
    on (
        full_responses.course_key = blocks.course_key
        and full_responses.problem_id = blocks.block_id
    )
left outer join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii users
    on (
        full_responses.actor_id like 'mailto:%'
        and SUBSTRING(full_responses.actor_id, 8) = users.email
    )
    or full_responses.actor_id = toString(users.external_user_id)

where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
