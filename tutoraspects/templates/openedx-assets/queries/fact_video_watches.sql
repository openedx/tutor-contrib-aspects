with watched_segments as (
    {% include 'openedx-assets/queries/fact_watched_video_segments.sql' %}
)

select
    org,
    course_key,
    course_name,
    course_run,
    video_name,
    video_name_with_location,
    actor_id,
    count(distinct segment_start) as watched_segment_count,
    (video_duration - 10) / 5 as video_segment_count,
    video_segment_count <= watched_segment_count as watched_entire_video
from watched_segments
group by
    org,
    course_key,
    course_name,
    course_run,
    video_name,
    video_name_with_location,
    actor_id,
    video_segment_count
