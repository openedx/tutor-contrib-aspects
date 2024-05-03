select results.*
from {{ DBT_PROFILE_TARGET_DATABASE }}.int_problem_results results
join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_at_risk_learners
        using (org, course_key, actor_id)
