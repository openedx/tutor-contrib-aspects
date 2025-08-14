select *
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_navigation_completion
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
