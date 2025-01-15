select
    fes.org,
    fes.course_key,
    fes.actor_id,
    fes.enrollment_status,
    fes.enrollment_mode,
    fes.emission_time,
    cn.course_name,
    cn.course_run
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_enrollment fes
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names cn
    on fes.org = cn.org
    and fes.course_key = cn.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
