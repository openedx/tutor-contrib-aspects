with video_plays as ({% include 'openedx-assets/queries/fact_video_plays.sql' %})

select video_plays.*
from video_plays
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
