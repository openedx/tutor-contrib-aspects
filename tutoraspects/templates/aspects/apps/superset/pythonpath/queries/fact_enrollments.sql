with courses as (
    {% include 'aspects/apps/superset/pythonpath/queries/dim_courses.sql' %}
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
