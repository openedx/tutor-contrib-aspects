select
    fact_pageview_engagement.*
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_pageview_engagement
join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_at_risk_learners
using (org, course_key, actor_id)
