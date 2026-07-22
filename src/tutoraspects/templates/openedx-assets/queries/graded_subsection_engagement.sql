select org, course_key, actor_id, subsection_number, subsection_with_name, scaled_score
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_problem_results
