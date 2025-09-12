select
    response.org as org,
    response.course_key as course_key,
    response.object_id as object_id,
    response.problem_id as problem_id,
    response.problem_link as problem_link,
    response.display_name_with_location as display_name_with_location,
    response.graded as graded,
    response.actor_id as actor_id,
    response.course_order as course_order,
    response.interaction_type as interaction_type,
    response.attempts as attempts,
    response.success as success,
    response.emission_time as emission_time,
    response.responses as responses,
    response.scaled_score as scaled_score
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_response response
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
