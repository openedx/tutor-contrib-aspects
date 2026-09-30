select distinct
    page.org as org,
    page.course_key as course_key,
    page.section_subsection_name as section_subsection_name,
    page.content_level as content_level,
    page.actor_id as actor_id,
    page.section_subsection_page_engagement as section_subsection_page_engagement,
    page.section_with_name as section_with_name,
    users.username as username,
    users.name as name,
    users.email as email
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_pageview_engagement page
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii users
    on (page.actor_id like 'mailto:%' and SUBSTRING(actor_id, 8) = users.email)
    or page.actor_id = toString(users.external_user_id)
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
