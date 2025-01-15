-- See learner_response_attempts.sql for more context
with
    successful_responses as (
        select
            org, course_key, problem_id, actor_id::String as actor_id, first_success_at
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_response_attempt
        where
            isNotNull(first_success_at)
            {% include 'openedx-assets/queries/common_filters.sql' %}
    ),
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
    ),
    -- Aggregating course-wide averages and percentages
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
        from full_responses
        group by org, course_key, problem_id
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
    users.name as name,
    -- Aggregated values from the coursewide_attempts CTE
    coursewide_attempts.avg_correct_attempts as avg_correct_attempts_coursewide,
    coursewide_attempts.avg_incorrect_attempts as avg_incorrect_attempts_coursewide,
    coursewide_attempts.coursewide_percent_correct as coursewide_percent_correct,
    -- Learner-specific calculations (correcting the percentage calculations)
    (
        case when full_responses.success then full_responses.attempts else 0 end
    ) as correct_attempts_by_learner,
    (
        case when not full_responses.success then full_responses.attempts else 0 end
    ) as incorrect_attempts_by_learner,
    -- Ensure we calculate percentage based on total attempts per problem (multiplied
    -- by 100 only once)
    (
        sum(case when full_responses.success then 1 else 0 end) over (
            partition by full_responses.actor_id, full_responses.problem_id
        ) / count(*) over (
            partition by full_responses.actor_id, full_responses.problem_id
        )
    ) as selected_learner_percent_correct,
    (
        sum(case when not full_responses.success then 1 else 0 end) over (
            partition by full_responses.actor_id, full_responses.problem_id
        ) / count(*) over (
            partition by full_responses.actor_id, full_responses.problem_id
        )
    ) as selected_learner_percent_incorrect
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
join
    coursewide_attempts
    on full_responses.org = coursewide_attempts.org
    and full_responses.course_key = coursewide_attempts.course_key
    and full_responses.problem_id = coursewide_attempts.problem_id
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
