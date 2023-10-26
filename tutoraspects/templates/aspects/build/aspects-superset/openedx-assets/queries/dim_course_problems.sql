select
    org,
    course_name,
    course_key,
    course_run,
    block_id as problem_id,
    block_name as problem_name,
    display_name_with_location as problem_name_with_location
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks
where
    problem_id like '%problem+block%'
{% raw -%}
    {% if filter_values('org') != [] %}
    and org in {{ filter_values('org') | where_in }}
    {% endif %}
    {% if filter_values('problem_name_with_location') != [] %}
    and problem_name_with_location in {{ filter_values('problem_name_with_location') | where_in }}
    {% endif %}
{%- endraw %}
