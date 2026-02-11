select
    status.org as org,
    status.course_key as course_key,
    names.course_name as course_name,
    names.course_run as course_run,
    status.actor_id as actor_id,
    sum(
        case when last_response.success and last_response.attempts = 1 then 1 else 0 end
    ) as first_try_correct_count,
    count(
        distinct case when last_response.attempts > 1 then last_response.object_id end
    ) as response_count,
    status.course_grade as course_grade,
    status.approving_state as approving_state
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status as status
join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on status.course_key = names.course_key
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_response as last_response
    on status.org = last_response.org
    and status.course_key = last_response.course_key
    and status.actor_id = last_response.actor_id
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
group by
    org, course_key, course_name, course_run, actor_id, course_grade, approving_state
