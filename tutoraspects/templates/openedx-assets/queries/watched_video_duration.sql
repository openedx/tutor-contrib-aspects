select
    names.org as org,
    names.course_key as course_key,
    names.course_name as course_name,
    names.course_run as course_run,
    actor_id,
    video_count,
    video_duration,
    watched_time,
    rewatched_time
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.watched_video_duration(
        {% raw -%}
        org_filter ={{ filter_values("org") }},
        course_name_filter ={{ filter_values("course_name") }}
        {%- endraw %}
    ) as a
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names as names
    on a.org = names.org
    and a.course_key = names.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
