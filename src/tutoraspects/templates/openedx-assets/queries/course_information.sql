select
    enrollment.org as org,
    names.course_name as course_name,
    names.course_run as course_run,
    enrollment.actor_id as actor_id,
    enrollment.enrollment_mode as enrollment_mode,
    case
        when last_course_visit.emission_time >= subtractDays(now(), 7)
        then enrollment.actor_id
        else null
    end as active_learner,
    tags.tag as course_tag,
    enrollment.course_key as course_key
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_enrollment enrollment
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_course_visit last_course_visit
    on enrollment.org = last_course_visit.org
    and enrollment.course_key = last_course_visit.course_key
    and enrollment.actor_id = last_course_visit.actor_id
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on enrollment.org = names.org
    and enrollment.course_key = names.course_key
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_course_tags tags
    on tags.course_key = enrollment.course_key
where
    enrollment.enrollment_status = 'registered'
    {% include 'openedx-assets/queries/common_filters.sql' %}
