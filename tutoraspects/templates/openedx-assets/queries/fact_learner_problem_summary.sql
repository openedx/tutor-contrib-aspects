with
    problem_responses as (
        {% include 'openedx-assets/queries/int_problem_responses.sql' %}
    ),
    outcomes as (
        select
            emission_time,
            org,
            course_key,
            problem_id,
            actor_id,
            success,
            first_value(success) over (
                partition by course_key, problem_id, actor_id order by success ASC
            ) as was_successful
        from problem_responses
    ),
    successful_responses as (
        select
            org,
            course_key,
            problem_id,
            actor_id,
            min(emission_time) as first_success_at
        from outcomes
        where was_successful = true and success = true
        group by org, course_key, problem_id, actor_id
    ),
    unsuccessful_responses as (
        select
            org,
            course_key,
            problem_id,
            actor_id,
            max(emission_time) as last_response_at
        from outcomes
        where was_successful = false
        group by org, course_key, problem_id, actor_id
    ),
    final_responses as (
        select org, course_key, problem_id, actor_id, first_success_at as emission_time
        from successful_responses
        union all
        select org, course_key, problem_id, actor_id, last_response_at as emission_time
        from unsuccessful_responses
    ),
    int_problem_results as (
        select
            emission_time,
            org,
            course_key,
            course_name,
            course_run,
            problem_id,
            problem_name,
            problem_name_with_location,
            actor_id,
            responses,
            success,
            attempts
        from problem_responses
        inner join
            final_responses using (org, course_key, problem_id, actor_id, emission_time)
    ),
    summary_base as (
        select
            org,
            course_key,
            course_name,
            course_run,
            problem_name,
            problem_name_with_location,
            actor_id,
            success,
            attempts,
            0 as num_hints_displayed,
            0 as num_answers_displayed
        from int_problem_results
        union all
        select
            org,
            course_key,
            course_name,
            course_run,
            problem_name,
            problem_name_with_location,
            actor_id,
            NULL as success,
            NULL as attempts,
            caseWithExpression(help_type, 'hint', 1, 0) as num_hints_displayed,
            caseWithExpression(help_type, 'answer', 1, 0) as num_answers_displayed
        from {{ DBT_PROFILE_TARGET_DATABASE }}.int_problem_hints
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    )

select
    org,
    course_key,
    course_name,
    course_run,
    problem_name,
    problem_name_with_location,
    actor_id,
    coalesce(any(success), false) as success,
    coalesce(any(attempts), 0) as attempts,
    sum(num_hints_displayed) as num_hints_displayed,
    sum(num_answers_displayed) as num_answers_displayed
from summary_base
where
    {% raw %}
    {% if get_filters("problem_name_with_location", remove_filter=True) == [] %} 1 = 1
    {% elif filter_values("problem_name_with_location") != [] %}
        problem_name_with_location
        in {{ filter_values("problem_name_with_location") | where_in }}
    {% else %} 1 = 0
    {% endif %}
    {% endraw %}
group by
    org,
    course_key,
    course_name,
    course_run,
    problem_name,
    problem_name_with_location,
    actor_id
