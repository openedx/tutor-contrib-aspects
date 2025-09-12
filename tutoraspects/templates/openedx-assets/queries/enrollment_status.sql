select
    enrollment.org,
    enrollment.course_key,
    enrollment.actor_id,
    enrollment.enrollment_status,
    enrollment.enrollment_mode,
    enrollment.emission_time,
    names.course_name,
    names.course_run
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_enrollment enrollment
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on enrollment.org = names.org
    and enrollment.course_key = names.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
