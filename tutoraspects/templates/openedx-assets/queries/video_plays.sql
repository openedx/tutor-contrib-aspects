with
    watched_video_segments as (
        {% include 'openedx-assets/queries/watched_video_segments.sql' %}
    ),
    segment_count as (
        select
            org,
            course_key,
            actor_id,
            video_link,
            section_with_name,
            subsection_with_name,
            segment_start,
            count(1) as segment_watch_count
        from watched_video_segments
        group by
            org,
            course_key,
            actor_id,
            video_link,
            section_with_name,
            subsection_with_name,
            segment_start
    )
select
    org,
    course_key,
    actor_id,
    video_link,
    section_with_name,
    subsection_with_name,
    max(segment_watch_count) as video_watch_count
from segment_count
group by org, course_key, actor_id, video_link, section_with_name, subsection_with_name