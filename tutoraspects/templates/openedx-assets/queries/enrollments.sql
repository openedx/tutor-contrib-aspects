with
    enrollments_base as (
        select *
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_enrollments
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    )

select
    emission_time,
    org,
    course_key,
    course_name,
    course_run,
    actor_id,
    enrollment_mode,
    enrollment_status
from enrollments_base
