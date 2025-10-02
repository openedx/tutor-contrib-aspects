select distinct
    navigation.org as org,
    navigation.course_key as course_key,
    navigation.block_id as block_id,
    navigation.course_order as course_order,
    navigation.actor_id as actor_id,
    navigation.page_count as page_count,
    navigation.section_with_name as section_with_name,
    navigation.subsection_with_name as subsection_with_name,
    navigation.visited_on as visited_on
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_navigation_completion navigation
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
