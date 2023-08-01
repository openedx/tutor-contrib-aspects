with enrollments as (
    select
        emission_time,
        org,
        course_key,
        actor_id,
        enrollment_mode,
        splitByString('/', verb_id)[-1] as enrollment_status
    from
        {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }}
    {% raw -%}
    {% if filter_values('org') != [] %}
    where
        org in ({{ filter_values('org') | where_in }})
    {% endif %}
    {%- endraw %}
)

select
    enrollments.emission_time,
    enrollments.org,
    courses.course_name,
    splitByString('+', courses.course_key)[-1] as run_name,
    enrollments.actor_id,
    enrollments.enrollment_mode,
    enrollments.enrollment_status
from
    enrollments
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
        on enrollments.course_key = courses.course_key
