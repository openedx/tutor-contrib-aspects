select distinct
    org,
    course_key,
    display_name as course_name,
    splitByString('+', course_key)[-1] as run_name
from
    {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
where
    location like '%course+block%'
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
