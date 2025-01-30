with
    watched_segments as (
        {% include 'openedx-assets/queries/watched_video_segments.sql' %}
    )

select
    org,
    course_key,
    course_name,
    course_run,
    section_with_name,
    subsection_with_name,
    video_name,
    video_name_with_location,
    video_link,
    actor_id,
    username,
    email,
    name,
    count(distinct segment_start) as watched_segment_count,
    (video_duration - 10) / 5 as video_segment_count,
    video_segment_count <= watched_segment_count as watched_entire_video
from watched_segments
where
    1 = 1
    {% raw %}
    {% if filter_values("Section Name") != [] %}
        and section_with_name in {{ filter_values("Section Name") | where_in }}
    {% endif %}
    {% if filter_values("Subsection Name") != [] %}
        and subsection_with_name in {{ filter_values("Subsection Name") | where_in }}
    {% endif %}
    {% if from_dttm %} and started_at > '{{ from_dttm }}' {% endif %}
    {% if to_dttm %} and started_at < '{{ to_dttm }}' {% endif %}
    {% endraw %}
group by
    org,
    course_key,
    course_name,
    course_run,
    section_with_name,
    subsection_with_name,
    video_name,
    video_name_with_location,
    video_link,
    actor_id,
    video_id,
    video_segment_count,
    username,
    email,
    name
