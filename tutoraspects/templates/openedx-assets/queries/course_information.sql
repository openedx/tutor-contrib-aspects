select
    fes.org as org,
    cn.course_name as course_name,
    course_run,
    fes.actor_id as actor_id,
    fes.enrollment_mode as enrollment_mode,
    case
        when flfc.emission_time >= subtractDays(now(), 7) then actor_id else null
    end as active_learner,
    tag as course_tag,
    fes.course_key as course_key
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_enrollment fes
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_course_visit flfc
    on fes.org = flfc.org
    and fes.course_key = flfc.course_key
    and fes.actor_id = flfc.actor_id
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names cn
    on fes.org = cn.org
    and fes.course_key = cn.course_key
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_course_tags mrct
    on mrct.course_key = fes.course_key
where
    enrollment_status = 'registered'
    {% include 'openedx-assets/queries/common_filters.sql' %}
