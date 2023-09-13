with problem_responses as (
    {% include 'openedx-assets/queries/int_problem_responses.sql' %}
)

select
    emission_time,
    org,
    course_key,
    course_name,
    course_run,
    problem_id,
    problem_name,
    actor_id,
    attempts,
    success,
    responses
from
    problem_responses
where
    {% raw %}
    {% if filter_values('problem_name') != [] %}
    problem_name in {{ filter_values('problem_name') | where_in }}
    {% else %}
    1=0
    {% endif %}
    {% endraw %}
