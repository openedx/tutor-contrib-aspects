with
    watched_video_segments as (
        {% include 'openedx-assets/queries/watched_video_segments.sql' %}
    ),
    final_results as (
        select
            org,
            course_key,
            video_name_location,
            video_link,
            actor_id,
            video_duration,
            username,
            email,
            name,
            count(segment_start) as _total_segments_watched,
            max(watched_count) as video_watched_count,
            max(
                case when watched_count > 1 then watched_count else 0 end
            ) as video_rewatched_count,
            section_with_name,
            subsection_with_name
        from watched_video_segments
        group by
            org,
            course_key,
            video_name_location,
            video_link,
            actor_id,
            username,
            email,
            name,
            video_duration,
            section_with_name,
            subsection_with_name
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
    video_watched_count,
    video_rewatched_count,
    _total_segments_watched / video_duration >= .95 as watched_entire_video,
    section_with_name,
    subsection_with_name
from final_results
