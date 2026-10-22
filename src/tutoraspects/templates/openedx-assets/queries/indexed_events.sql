with
    events as (
        select
            event_id,
            CAST(emission_time, 'DateTime') as emission_time,
            actor_id,
            object_id,
            splitByString('/', course_id)[-1] as course_key,
            org,
            verb_id
        from {{ ASPECTS_XAPI_DATABASE }}.xapi_events_all_parsed
    )

select
    courses.course_name as course_name,
    courses.course_run as course_run,
    event_id,
    actor_id,
    object_id,
    events.course_key,
    events.org,
    events.verb_id,
    emission_time
from events
join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names courses
    on (events.course_key = courses.course_key)
