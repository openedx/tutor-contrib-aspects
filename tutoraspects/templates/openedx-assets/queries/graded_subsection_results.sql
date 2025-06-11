select
    org,
    course_key,
    block_id_short as block_id,
    problem_number,
    actor_id,
    success,
    problem_name_location
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_problem_results
