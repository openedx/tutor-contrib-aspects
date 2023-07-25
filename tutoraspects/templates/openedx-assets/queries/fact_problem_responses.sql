with course_problems as (
     {% include 'openedx-assets/queries/dim_course_problems.sql' %}
), responses as (
    select
        emission_time,
        org,
        course_key,
        problem_id,
        actor_id,
        responses,
        success,
        attempts
    from
        {{ DBT_PROFILE_TARGET_DATABASE }}.problem_responses
    {% raw -%}
    {% if filter_values('org') != [] %}
    where
        org in {{ filter_values('org') | where_in }}
    {% endif %}
    {%- endraw %}
)

select
    responses.emission_time as emission_time,
    course_problems.org as org,
    course_problems.course_name as course_name,
    course_problems.run_name as run_name,
    course_problems.problem_name as problem_name,
    responses.actor_id as actor_id,
    responses.responses as responses,
    responses.success as success,
    responses.attempts as attempts
from
    responses
    join course_problems
        on (responses.org = course_problems.org
            and responses.course_key = course_problems.course_key
            and responses.problem_id = course_problems.problem_id)
