select
    results.org as org,
    results.course_key as course_key,
    results.block_id_short as block_id,
    results.problem_number as problem_number,
    results.actor_id as actor_id,
    results.success as success,
    results.problem_name_location as problem_name_location
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_problem_results results
