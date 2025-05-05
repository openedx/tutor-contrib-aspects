select
    last_response.org as org,
    last_response.course_key as course_key,
    blocks.course_name as course_name,
    blocks.course_run as course_run,
    last_response.actor_id as actor_id,
    last_response.success as success,
    last_response.attempts as attempts,
    status.course_grade as course_grade,
    status.approving_state as approving_state
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_response as last_response
join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
    on (
        last_response.course_key = blocks.course_key
        and last_response.problem_id = blocks.block_id
    )
join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status status
    on status.org = last_response.org
    and status.course_key = last_response.course_key
    and status.actor_id = last_response.actor_id
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
