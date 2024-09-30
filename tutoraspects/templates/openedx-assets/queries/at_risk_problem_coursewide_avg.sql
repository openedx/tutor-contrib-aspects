with
    problem_coursewide_avg as (
        {% include 'openedx-assets/queries/problem_coursewide_avg.sql' %}
    )

select problem_coursewide_avg.*
from problem_coursewide_avg
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
