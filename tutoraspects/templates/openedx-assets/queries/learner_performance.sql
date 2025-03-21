-- select one record per (learner, problem, course, org) tuple
-- contains either the first successful attempt
-- or the most recent unsuccessful attempt
-- find the timestamp of the earliest successful response
-- this will be used to pick the xAPI event corresponding to that submission
with
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
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_response_attempt
        join
            {{ ASPECTS_XAPI_DATABASE }}.problem_events events using (
                org, course_key, problem_id, actor_id, emission_time
            )
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    ),
    int_problem_results as (
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
                blocks.display_name_with_location,
                '</a>'
            ) as problem_link,
            full_responses.actor_id as actor_id,
            full_responses.responses as responses,
            full_responses.success as success,
            full_responses.attempts as attempts,
            full_responses.interaction_type as interaction_type,
            blocks.graded
        from full_responses
        join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
            on (
                full_responses.course_key = blocks.course_key
                and full_responses.problem_id = blocks.block_id
            )
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    )

select
    org,
    course_key,
    course_name,
    course_run,
    actor_id,
    success,
    attempts,
    course_grade,
    approving_state
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status
left join int_problem_results
using org, course_key, course_run, actor_id, course_name
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
