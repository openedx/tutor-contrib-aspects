with
    fact_problem_engagement as (
        {% include 'openedx-assets/queries/fact_problem_engagement.sql' %}
    )
select fact_problem_engagement.*
from fact_problem_engagement pe
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners
    on (
        pe.org = at_risk_learners.org
        and pe.course_key = at_risk_learners.course_key
        and pe.actor_id = at_risk_learners.actor_id
    )
