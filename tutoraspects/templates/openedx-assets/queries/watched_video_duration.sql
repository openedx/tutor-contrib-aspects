with
    video_events as (
        select *, splitByString('/xblock/', object_id)[-1] as video_id
        from {{ ASPECTS_XAPI_DATABASE }}.video_playback_events
    ),
    totals as (
        select
            org,
            course_key,
            count(distinct video_id) as count_videos,
            avg(video_duration) as avg_video_length
        from video_events
        group by org, course_key
    ),
    starts as (
        select
            org,
            course_key,
            actor_id,
            emission_time,
            cast(video_position as Int32) as start_position,
            video_id,
            video_duration
        from video_events
        where verb_id = 'https://w3id.org/xapi/video/verbs/played'
    ),
    ends as (
        select
            org,
            course_key,
            actor_id,
            emission_time,
            cast(video_position as Int32) as end_position,
            video_id
        from video_events
        where
            verb_id in (
                'http://adlnet.gov/expapi/verbs/completed',
                'https://w3id.org/xapi/video/verbs/seeked',
                'https://w3id.org/xapi/video/verbs/paused',
                'http://adlnet.gov/expapi/verbs/terminated'
            )
    ),
    rewatches as (
        select org, course_key, video_id, actor_id, start_position
        from starts
        group by org, course_key, video_id, actor_id, start_position
        having count(1) > 1
    ),
    duration as (
        select
            starts.org as org,
            starts.course_key as course_key,
            starts.actor_id as actor_id,
            video_duration,
            starts.start_position - end_position as watched_duration,
            case when rewatches.org <> '' then 1 else 0 end as rewatched
        from starts left
        asof join
            ends
            on starts.org = ends.org
            and starts.course_key = ends.course_key
            and starts.video_id = ends.video_id
            and starts.actor_id = ends.actor_id
            and starts.emission_time < ends.emission_time
        left join
            rewatches
            on rewatches.org = starts.org
            and rewatches.course_key = starts.course_key
            and rewatches.actor_id = starts.actor_id
            and rewatches.start_position = starts.start_position
            and rewatches.video_id = starts.video_id
    )
select
    totals.org as org,
    names.course_name as course_name,
    names.course_run as course_run,
    duration.course_key as course_key,
    count_videos,
    avg_video_length,
    video_duration,
    watched_duration,
    rewatched
from duration
left join totals
using org, course_key
left join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names as names
using org, course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
