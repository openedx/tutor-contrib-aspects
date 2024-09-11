select
    names.org as org,
    names.course_key as course_key,
    names.course_name as course_name,
    names.course_run as course_run,
    actor_id,
    video_id,
    video_duration,
    watched_time,
    rewatched_time
from event_sink.watched_video_duration
left join event_sink.course_names as names
using org, course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
