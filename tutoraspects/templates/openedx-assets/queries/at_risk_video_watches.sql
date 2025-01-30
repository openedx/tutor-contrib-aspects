with watches as ({% include 'openedx-assets/queries/video_watches.sql' %})

select watches.*
from watches
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
