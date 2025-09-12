select
    fact_enrollments.emission_time as emission_time,
    fact_enrollments.org as org,
    fact_enrollments.course_key as course_key,
    names.course_name as course_name,
    names.course_run as course_run,
    fact_enrollments.actor_id as actor_id,
    fact_enrollments.enrollment_mode as enrollment_mode,
    fact_enrollments.enrollment_status as enrollment_status
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_enrollments
join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on fact_enrollments.course_key = names.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
