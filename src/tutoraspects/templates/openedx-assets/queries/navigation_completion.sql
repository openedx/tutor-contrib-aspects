select
    navigation.org as org,
    navigation.course_key as course_key,
    navigation.block_id as block_id,
    navigation.course_order as course_order,
    navigation.actor_id as actor_id,
    navigation.page_count as page_count,
    navigation.section_with_name as section_with_name,
    navigation.subsection_with_name as subsection_with_name,
    navigation.visited_on as visited_on,
    navigation.subsection_block_id as subsection_block_id,
    navigation.section_block_id as section_block_id
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_navigation_completion navigation
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
