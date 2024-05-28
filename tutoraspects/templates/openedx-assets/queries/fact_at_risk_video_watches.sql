with watches as ({% include 'openedx-assets/queries/fact_video_watches.sql' %})

select watches.*
from watches
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
