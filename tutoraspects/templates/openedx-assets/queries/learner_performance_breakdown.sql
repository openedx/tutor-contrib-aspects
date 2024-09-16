select
    org,
    actor_id,
    course_name,
    course_run,
    approving_state,
    case
        when fllcv.emission_time >= subtractDays(now(), 7)
        then 'active'
        when
            fllcv.emission_time < subtractDays(now(), 7)
            and approving_state = 'failed'
            and enrollment_status = 'registered'
        then 'at-risk'
        else 'other'
    end as learner_status,
    fss.course_key as course_key
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_student_status fss
left join {{ ASPECTS_XAPI_DATABASE }}.fact_learner_last_course_visit fllcv
using org, course_key, actor_id
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
