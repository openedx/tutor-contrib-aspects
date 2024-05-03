with segment_watches as (
  {% include 'openedx-assets/queries/fact_watched_video_segments.sql' %}
)

select segment_watches.*
from segment_watches
join {{ DBT_PROFILE_TARGET_DATABASE }}.dim_at_risk_learners
using (org, course_key, actor_id)
