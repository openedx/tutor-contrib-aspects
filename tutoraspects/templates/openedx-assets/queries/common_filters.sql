{% raw -%}
{% if filter_values('org') != [] %}
and org in {{ filter_values('org') | where_in }}
{% endif %}

{% if filter_values('course_name') != [] %}
and course_key in (
    select course_key
    from {% endraw -%}{{ ASPECTS_EVENT_SINK_DATABASE }}.course_names{%- raw %}
    where course_name in {{ filter_values('course_name') | where_in }}
)
{% endif %}
{%- endraw %}
