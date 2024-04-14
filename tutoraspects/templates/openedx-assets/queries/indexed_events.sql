with events as (
  SELECT
    event_id,
    CAST(emission_time, 'DateTime') AS emission_time,
    actor_id,
    object_id,
    splitByString('/', course_id)[-1] AS course_key,
    org,
    verb_id
  FROM {{ ASPECTS_XAPI_DATABASE }}.xapi_events_all_parsed
)

SELECT
  courses.course_name as course_name,
  courses.course_run as course_run,
  event_id,
  actor_id,
  object_id,
  events.course_key,
  events.org,
  events.verb_id,
  emission_time
FROM events
JOIN
   {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
ON
  (events.course_key = courses.course_key)
