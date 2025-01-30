with
    problem_engagement_sql as (
        {% include 'openedx-assets/queries/problem_engagement.sql' %}
    )
select problem_engagement_sql.*
from problem_engagement_sql pe
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners
    on (
        pe.org = at_risk_learners.org
        and pe.course_key = at_risk_learners.course_key
        and pe.actor_id = at_risk_learners.actor_id
    )
