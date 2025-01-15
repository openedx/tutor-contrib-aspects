{% raw -%}
{% if filter_values("org") != [] %}
    and org in {{ filter_values("org") | where_in }}
{% endif %}

{% if filter_values("course_name") != [] %}
    and course_key in (
        select course_key
        from {% endraw -%} {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names{%- raw %}
        where course_name in {{ filter_values("course_name") | where_in }}
    )
{% endif %}
{%- endraw %}

{% raw -%}
{% if filter_values("tag") != [] %}
    and course_key in (
        select course_key
        from
            {% endraw -%} {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_course_tags{%- raw %}
        where
            tag in (select replaceAll(arrayJoin({{ filter_values("tag") }}), '- ', ''))
    )
{% endif %}
{%- endraw %}
