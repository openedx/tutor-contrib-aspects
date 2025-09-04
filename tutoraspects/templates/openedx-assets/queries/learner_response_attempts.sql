select *
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_response
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
