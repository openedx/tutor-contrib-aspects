with video_plays as ({% include 'openedx-assets/queries/video_plays.sql' %})

select video_plays.*
from video_plays
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
