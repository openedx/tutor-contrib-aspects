select fact_video_engagement.*
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_engagement
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
