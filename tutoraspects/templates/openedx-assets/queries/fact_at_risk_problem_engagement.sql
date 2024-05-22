{% include 'openedx-assets/queries/fact_problem_engagement.sql' %}
join (
    {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
) as at_risk_learners
using (org, course_key, actor_id)
