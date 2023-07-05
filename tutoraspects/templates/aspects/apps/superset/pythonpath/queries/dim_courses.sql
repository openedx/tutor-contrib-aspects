select distinct
    org,
    course_key,
    display_name as course_name,
    location as run_id,
    JSON_VALUE(xblock_data_json, '$.run') as run_name
from
    {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
where
    JSON_VALUE(xblock_data_json, '$.block_type') = 'course'
{% raw -%}
    {% if filter_values('org') != [] %}
    and org in {{ filter_values('org') | where_in }}
    {% endif %}
    {% if filter_values('course_name') != [] %}
    and display_name in {{ filter_values('course_name') | where_in }}
    {% endif %}
    {% if filter_values('run') != [] %}
    and run_name in {{ filter_values('run') | where_in }}
    {% endif %}
{%- endraw %}
