with transcripts as (
select *
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_transcript_usage
where
    {% raw %}
    {% if get_filters('course_name', remove_filter=True) == [] %}
    1=1
    {% elif filter_values('course_name') != [] %}
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
from transcripts
