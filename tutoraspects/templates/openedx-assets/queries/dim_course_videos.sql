with video_blocks as (
    select
        org,
        course_key,
        location as video_id,
        display_name as video_name
    from
        {{ ASPECTS_EVENT_SINK_DATABASE }}.{{ ASPECTS_EVENT_SINK_NODES_TABLE }}
    where
    {% raw -%}
        location like '%video+block%'
        {% if filter_values('org') != [] %}
        and org in {{ filter_values('org') | where_in }}
        {% endif %}
        {% if filter_values('video_name') != [] %}
        and video_name in {{ filter_values('video_name') | where_in }}
        {% endif %}
    {%- endraw %}
)

select
    course_names.org as org,
    course_names.course_name as course_name,
    course_names.course_key as course_key,
    course_names.course_run as course_run,
    video_blocks.video_id as video_id,
    video_blocks.video_name as video_name
from
    {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names course_names
    join video_blocks
        on (course_names.org = video_blocks.org
            and course_names.course_key = video_blocks.course_key)
