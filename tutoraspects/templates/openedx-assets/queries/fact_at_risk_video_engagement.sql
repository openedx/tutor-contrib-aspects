with engagement as (
  {% include 'openedx-assets/queries/fact_video_engagement.sql' %}
)

select *
from engagement
join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_at_risk_learners
using (org, course_key, actor_id)