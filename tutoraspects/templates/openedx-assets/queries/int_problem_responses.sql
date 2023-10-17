with problem_responses as (
select *
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_problem_responses
where 1=1
    {% include 'openedx-assets/queries/common_filters.sql' %}
)

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
    attempts,
    success,
    responses
from
    problem_responses
