select fact_problem_engagement.*
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_problem_engagement
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners
    on (
        fact_problem_engagement.org = at_risk_learners.org
        and fact_problem_engagement.course_key = at_risk_learners.course_key
        and fact_problem_engagement.actor_id = at_risk_learners.actor_id
    )
