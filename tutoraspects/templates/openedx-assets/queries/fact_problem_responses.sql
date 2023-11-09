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
    problem_name_with_location,
    actor_id,
    attempts,
    success,
    arrayJoin(
        if(
            JSONArrayLength(responses) > 0,
            JSONExtractArrayRaw(responses),
            [responses]
        )
    ) as responses
from
    problem_responses
where
    {% raw %}
    {% if filter_values('problem_name_with_location') != [] %}
    problem_name_with_location in {{ filter_values('problem_name_with_location') | where_in }}
    {% else %}
    1=0
    {% endif %}
    {% endraw %}
