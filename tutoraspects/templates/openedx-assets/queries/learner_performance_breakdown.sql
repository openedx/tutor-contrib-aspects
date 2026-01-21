select
    status.org as org,
    status.actor_id as actor_id,
    names.course_name as course_name,
    names.course_run as course_run,
    status.approving_state as approving_state,
    case
        when status.last_navigated >= subtractDays(now(), 7)
        then 'active'
        when
            status.last_navigated < subtractDays(now(), 7)
            and status.approving_state = 'failed'
            and status.enrollment_status = 'registered'
        then 'at-risk'
        else 'other'
    end as learner_status,
    status.course_key as course_key,
    concat(names.course_run, ' - ', names.course_name) as run_name,
    concat(names.course_name, ' - ', status.org) as name_org
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status status
join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on status.course_key = names.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
