with
    watched_video_segments as (
        {% include 'openedx-assets/queries/watched_video_segments.sql' %}
    )

select
    org,
    course_key,
    video_name_location,
    video_link,
    actor_id,
    username,
    email,
    name,
    count(distinct segment_start) as watched_segment_count,
    video_duration <= watched_segment_count as watched_entire_video
from watched_video_segments
group by
    org,
    course_key,
    video_name_location,
    video_link,
    actor_id,
    video_duration,
    username,
    email,
    name
