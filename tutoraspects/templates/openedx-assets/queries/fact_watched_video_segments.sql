with video_events as (
    select
        emission_time,
        org,
        course_key,
        splitByString('/xblock/', object_id)[-1] as video_id,
        actor_id,
        verb_id,
        video_position
    from {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}
    where 1=1
    {% include 'openedx-assets/queries/common_filters.sql' %}
), starts as (
    select *
    from video_events
    where verb_id = 'https://w3id.org/xapi/video/verbs/played'
), ends as (
    select *
    from video_events
    where
        verb_id in (
            'http://adlnet.gov/expapi/verbs/completed',
            'https://w3id.org/xapi/video/verbs/seeked',
            'https://w3id.org/xapi/video/verbs/paused',
            'http://adlnet.gov/expapi/verbs/terminated'
        )
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
        segments.course_key as course_key,
        blocks.course_name as course_name,
        blocks.course_run as course_run,
        blocks.block_name as video_name,
        blocks.display_name_with_location as video_name_with_location,
        segments.actor_id as actor_id,
        segments.started_at as started_at,
        segments.start_position - (segments.start_position % 5) as start_position,
        segments.end_position - (segments.end_position % 5) as end_position
    from
        segments
        join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
            on (segments.course_key = blocks.course_key
                and segments.video_id = blocks.block_id)
)

select
    org,
    course_key,
    course_name,
    course_run,
    video_name,
    video_name_with_location,
    actor_id,
    started_at,
    arrayJoin(range(start_position, end_position, 5)) as segment_start
from enriched_segments
where
    {% raw %}
    {% if filter_values('video_name_with_location') != [] %}
    video_name_with_location in {{ filter_values('video_name_with_location') | where_in }}
    {% else %}
    1=0
    {% endif %}
    {% endraw %}
