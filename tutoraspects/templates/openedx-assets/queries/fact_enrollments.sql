with courses as (
    {% include 'openedx-assets/queries/dim_courses.sql' %}
), enrollments as (
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
    courses.run_name,
    enrollments.actor_id,
    enrollments.enrollment_mode,
    enrollments.enrollment_status
from
    enrollments
    join courses
        on (enrollments.org = courses.org
            and enrollments.course_key = courses.course_key)
