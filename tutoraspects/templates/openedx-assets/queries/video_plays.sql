with
    plays as (
        select *
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_plays
        where
            {% raw %}
            {% if get_filters("course_name", remove_filter=True) == [] %} 1 = 1
            {% elif filter_values("course_name") != [] %}
                course_name in {{ filter_values("course_name") | where_in }}
            {% else %} 1 = 0
            {% endif %}
            {% endraw %}
            {% include 'openedx-assets/queries/common_filters.sql' %}
    )

select *
from plays
