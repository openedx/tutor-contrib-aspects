with starts as (
    select
        emission_time,
        org,
        course_key,
        splitByString('/xblock/', object_id)[-1] as video_id,
        actor_id,
        verb_id,
        video_position
    from {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}
    where
        verb_id = 'https://w3id.org/xapi/video/verbs/played'
        {% raw -%}
        {% if filter_values('org') != [] %}
        and org in {{ filter_values('org') | where_in }}
        {% endif %}
        {%- endraw %}
), ends as (
    select
        emission_time,
        org,
        course_key,
        splitByString('/xblock/', object_id)[-1] as video_id,
        actor_id,
        verb_id,
        video_position
    from {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}
    where
        verb_id in (
            'http://adlnet.gov/expapi/verbs/completed',
            'https://w3id.org/xapi/video/verbs/seeked',
            'https://w3id.org/xapi/video/verbs/paused',
            'http://adlnet.gov/expapi/verbs/terminated'
        )
        {% raw -%}
        {% if filter_values('org') != [] %}
        and org in {{ filter_values('org') | where_in }}
        {% endif %}
        {%- endraw %}
), segments as(
    select
        starts.org as org,
        starts.course_key as course_key,
        starts.video_id as video_id,
        starts.actor_id,
        cast(starts.video_position as Int32) as start_position,
        cast(ends.video_position as Int32) as end_position,
        starts.emission_time as started_at,
        ends.emission_time as ended_at,
        ends.verb_id as end_type
    from
        starts
        left asof join ends
            on (starts.org = ends.org
                and starts.course_key = ends.course_key
                and starts.video_id = ends.video_id
                and starts.actor_id = ends.actor_id
                and starts.emission_time < ends.emission_time)
), enriched_segments as (
    select
        segments.org as org,
        courses.course_name as course_name,
        splitByString('+', courses.course_key)[-1] as run_name,
        blocks.block_name as video_name,
        segments.actor_id as actor_id,
        segments.started_at as started_at,
        segments.start_position - (segments.start_position % 5) as start_position,
        segments.end_position - (segments.end_position % 5) as end_position
    from
        segments
        join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
            on segments.course_key = courses.course_key
        join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names blocks
            on segments.video_id = blocks.location
)

select
    org,
    course_name,
    run_name,
    video_name,
    actor_id,
    started_at,
    arrayJoin(range(start_position, end_position, 5)) as segment_start
from enriched_segments
