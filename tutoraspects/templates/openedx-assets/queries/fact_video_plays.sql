with plays as (
select *
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_plays
where
    {% raw %}
    {% if filter_values('course_name') != [] %}
    course_name in {{ filter_values('course_name') | where_in }}
    {% else %}
    1=0
    {% endif %}
    {% endraw %}
    {% include 'openedx-assets/queries/common_filters.sql' %}
)

select
    emission_time,
    org,
    course_key,
    course_name,
    course_run,
    video_name,
    video_name_with_location,
    actor_id
from plays
