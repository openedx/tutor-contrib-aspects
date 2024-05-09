select
    fact_video_engagement.*
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_engagement
join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_at_risk_learners
using (org, course_key, actor_id)
