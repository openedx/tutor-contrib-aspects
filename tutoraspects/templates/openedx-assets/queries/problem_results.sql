select
    results.org as org,
    results.course_key as course_key,
    results.success as success,
    results.attempts as attempts,
    results.actor_id as actor_id,
    results.problem_location as problem_location,
    results.problem_name_location as problem_name_location,
    results.block_id_short as block_id,
    concat('#', splitByString('_', results.problem_location)[2]) as problem_part
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_problem_results results
