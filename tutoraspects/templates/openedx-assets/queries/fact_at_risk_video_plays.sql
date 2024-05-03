with video_plays as (
  {% include 'openedx-assets/queries/fact_video_plays.sql' %}
)

select video_plays.*
from video_plays
join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_at_risk_learners
using (org, course_key, actor_id)
