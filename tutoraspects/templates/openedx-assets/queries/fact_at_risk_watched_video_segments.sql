select watches.*
from {{ DBT_PROFILE_TARGET_DATABASE}}.fact_watched_video_segments watches
join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_at_risk_learners
using (org, course_key, actor_id)
