select
    status.org as org,
    names.course_name as course_name,
    names.course_run as course_run,
    status.actor_id as actor_id,
    status.enrollment_mode as enrollment_mode,
    case
        when status.last_navigated >= subtractDays(now(), 7)
        then status.actor_id
        else null
    end as active_learner,
    tags.tag as course_tag,
    status.course_key as course_key
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status status
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on status.org = names.org
    and status.course_key = names.course_key
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_course_tags tags
    on tags.course_key = status.course_key
where
    status.enrollment_status = 'registered'
    {% include 'openedx-assets/queries/common_filters.sql' %}
