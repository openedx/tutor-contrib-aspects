select
    status.org as org,
    status.course_key as course_key,
    status.actor_id as actor_id,
    status.approving_state as approving_state,
    status.enrollment_mode as enrollment_mode,
    status.enrollment_status as enrollment_status,
    status.course_grade as course_grade,
    status.grade_bucket as grade_bucket,
    users.username as username,
    users.name as name,
    users.email as email,
    status.enrolled_at as enrolled_at,
    at_risk_learners.last_visited as last_visited,
    names.course_name as course_name,
    names.course_run as course_run
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status status
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii users
    on (status.actor_id like 'mailto:%' and SUBSTRING(status.actor_id, 8) = users.email)
    or status.actor_id = toString(users.external_user_id)
join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on status.course_key = names.course_key
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners
    on status.org = at_risk_learners.org
    and status.course_key = at_risk_learners.course_key
    and status.actor_id = at_risk_learners.actor_id
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
