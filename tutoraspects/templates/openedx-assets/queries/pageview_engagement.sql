select fact_pageview_engagement.*
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_pageview_engagement
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
