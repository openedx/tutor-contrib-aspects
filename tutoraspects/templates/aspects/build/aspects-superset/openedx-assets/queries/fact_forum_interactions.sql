select *
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_forum_interactions
where 1=1
    {% include 'aspects/build/aspects-superset/openedx-assets/queries/common_filters.sql' %}
