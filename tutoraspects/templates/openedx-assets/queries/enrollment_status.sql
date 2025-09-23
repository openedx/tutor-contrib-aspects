select
    enrollment.emission_time as emission_time,
    enrollment.org as org,
    enrollment.course_key as course_key,
    names.course_name as course_name,
    names.course_run as course_run,
    enrollment.actor_id as actor_id,
    enrollment.enrollment_mode as enrollment_mode,
    enrollment.enrollment_status as enrollment_status
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_enrollment enrollment
join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on enrollment.course_key = names.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
