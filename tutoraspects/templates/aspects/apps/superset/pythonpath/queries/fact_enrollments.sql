{%- raw -%}
with courses as (
    select
        org,
        course_key,
        course_name,
        run_name
    from
        {{ dataset(24) }}
), enrollments as (
    select
        emission_time,
        org,
        splitByString('/', course_id)[-1] as course_key,
        actor_id,
        enrollment_mode,
        splitByString('/', verb_id)[-1] as enrollment_status
    from
        xapi.enrollment_events
    {% if filter_values('org') != [] %}
    where org in {{ filter_values('org') | where_in }}
    {% endif %}
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
        using (org, course_key)
{%- endraw -%}
