with problems as (
    select
        org,
        course_key,
        location as problem_id,
        display_name as problem_name
    from
        {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
    where
        location like '%problem+block%'
    {% raw -%}
        {% if filter_values('org') != [] %}
        and org in {{ filter_values('org') | where_in }}
        {% endif %}
        {% if filter_values('problem_name') != [] %}
        and problem_name in {{ filter_values('problem_name') | where_in }}
        {% endif %}
    {%- endraw %}
)

select
    course_names.org as org,
    course_names.course_name as course_name,
    course_names.course_key as course_key,
    course_names.course_run as course_run,
    problems.problem_id as problem_id,
    problems.problem_name as problem_name
from
    problems
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names course_names
        on (problems.org = course_names.org
            and problems.course_key = course_names.course_key)
