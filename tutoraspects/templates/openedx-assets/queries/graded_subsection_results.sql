select
    results.org as org,
    results.course_key as course_key,
    results.actor_id as actor_id,
    results.subsection_number as subsection_number,
    results.subsection_with_name as subsection_with_name,
    results.scaled_score as scaled_score,
    results.block_id_short as block_id,
    results.problem_number as problem_number,
    results.success as success,
    results.problem_name_location as problem_name_location
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_problem_results results
