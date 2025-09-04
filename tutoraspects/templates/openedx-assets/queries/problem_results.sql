select
    org,
    course_key,
    success,
    attempts,
    actor_id,
    problem_number,
    problem_name_location,
    block_id_short as block_id,
    concat('#', splitByString('_', problem_number)[2]) as problem_part
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_problem_results
