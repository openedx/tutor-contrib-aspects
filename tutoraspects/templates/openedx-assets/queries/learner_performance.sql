select
    org,
    course_key,
    course_name,
    course_run,
    actor_id,
    success,
    attempts,
    course_grade,
    approving_state
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_student_status
left join {{ DBT_PROFILE_TARGET_DATABASE }}.int_problem_results
using org, course_key, course_run, actor_id, course_name
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
