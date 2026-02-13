select
    status.org as org,
    status.actor_id as actor_id,
    status.course_name as course_name,
    status.course_run as course_run,
    status.approving_state as approving_state,
    case
        when last_course_visit.emission_time >= subtractDays(now(), 7)
        then 'active'
        when
            last_course_visit.emission_time < subtractDays(now(), 7)
            and status.approving_state = 'failed'
            and status.enrollment_status = 'registered'
        then 'at-risk'
        else 'other'
    end as learner_status,
    status.course_key as course_key,
    concat(status.course_run, ' - ', status.course_name) as run_name,
    concat(status.course_name, ' - ', status.org) as name_org
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status status
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_course_visit last_course_visit
using org, course_key, actor_id
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
