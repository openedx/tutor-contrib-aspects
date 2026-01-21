select
    status.org as org,
    status.course_key as course_key,
    status.actor_id as actor_id,
    status.last_navigated as last_visited
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status status
where
    status.last_navigated < subtractDays(now(), 7)
    and status.approving_state = 'failed'
    and status.enrollment_status = 'registered'
    {% include 'openedx-assets/queries/common_filters.sql' %}
