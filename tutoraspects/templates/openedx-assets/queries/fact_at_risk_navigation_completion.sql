select
    fnc.*
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.fact_navigation_completion fnc
    join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_at_risk_learners
        using (org, course_key, actor_id)
