with
    coursewide_attempts as (
        select
            org,
            course_key,
            problem_id,
            avg(case when success then attempts else 0 end) as avg_correct_attempts,
            avg(
                case when not success then attempts else 0 end
            ) as avg_incorrect_attempts,
            sum(case when success then 1 else 0 end)::float
            / count(*) as coursewide_percent_correct
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_response
        group by org, course_key, problem_id
    )
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
    last_response.attempts as attempts,
    last_response.interaction_type as interaction_type,
    blocks.graded as graded,
    users.username as username,
    users.email as email,
    users.name as name,
    -- Aggregated values from the coursewide_attempts CTE
    coursewide_attempts.avg_correct_attempts as avg_correct_attempts_coursewide,
    coursewide_attempts.avg_incorrect_attempts as avg_incorrect_attempts_coursewide,
    coursewide_attempts.coursewide_percent_correct as coursewide_percent_correct,
    -- Learner-specific calculations (correcting the percentage calculations)
    (
        case when last_response.success then last_response.attempts else 0 end
    ) as correct_attempts_by_learner,
    (
        case when not last_response.success then last_response.attempts else 0 end
    ) as incorrect_attempts_by_learner,
    -- Ensure we calculate percentage based on total attempts per problem (multiplied
    -- by 100 only once)
    (
        sum(case when last_response.success then 1 else 0 end) over (
            partition by last_response.actor_id, last_response.problem_id
        ) / count(*) over (
            partition by last_response.actor_id, last_response.problem_id
        )
    ) as selected_learner_percent_correct,
    (
        sum(case when not last_response.success then 1 else 0 end) over (
            partition by last_response.actor_id, last_response.problem_id
        ) / count(*) over (
            partition by last_response.actor_id, last_response.problem_id
        )
    ) as selected_learner_percent_incorrect
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_response last_response
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
    or full_responses.actor_id = toString(users.external_user_id)
join
    coursewide_attempts
    on last_response.org = coursewide_attempts.org
    and last_response.course_key = coursewide_attempts.course_key
    and last_response.problem_id = coursewide_attempts.problem_id
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
