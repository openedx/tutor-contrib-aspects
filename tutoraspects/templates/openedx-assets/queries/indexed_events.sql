select
    names.course_name as course_name,
    names.course_run as course_run,
    events.event_id as event_id,
    events.actor_id as actor_id,
    events.object_id as object_id,
    splitByString('/', events.course_id)[-1] as course_key,
    events.org as org,
    events.verb_id as verb_id,
    CAST(emission_time, 'DateTime') as emission_time
from {{ ASPECTS_XAPI_DATABASE }}.xapi_events_all_parsed events
join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on (events.course_key = names.course_key)
