with courses as (
    {% include 'openedx-assets/queries/dim_courses.sql' %}
), problems as (
    select
        org,
        course_key,
        location as problem_id,
        display_name as problem_name
    from
        {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
    where
        JSON_VALUE(xblock_data_json, '$.block_type') = 'problem'
    {% raw -%}
        {% if filter_values('org') != [] %}
        and org in ({{ filter_values('org') | where_in }})
        {% endif %}
        {% if filter_values('problem_name') != [] %}
        and problem_name in ({{ filter_values('problem_name') | where_in }})
        {% endif %}
    {%- endraw %}
)

select
    courses.org as org,
    courses.course_name as course_name,
    courses.course_key as course_key,
    courses.run_name as run_name,
    problems.problem_id as problem_id,
    problems.problem_name as problem_name
from
    problems
    join courses
        on (problems.org = courses.org
            and problems.course_key = courses.course_key)
