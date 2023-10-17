with grades as (
    select *
    from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_grades
    where
        grade_type = 'problem'

        {% raw %}
        {% if filter_values('problem_name_with_location') != [] %}
        and entity_name_with_location in {{ filter_values('problem_name_with_location', remove_filter=True) | where_in }}
        {% else %}
        and 1=0
        {% endif %}
        {% endraw %}

        {% include 'openedx-assets/queries/common_filters.sql' %}
),
most_recent_grades as (
    select
        org,
        course_key,
        entity_id,
        actor_id,
        max(emission_time) as emission_time
    from
        grades
    group by
        org,
        course_key,
        entity_id,
        actor_id
)

select
    grades.emission_time as emission_time,
    grades.org as org,
    grades.course_key as course_key,
    grades.course_name as course_name,
    grades.course_run as course_run,
    grades.entity_name as entity_name,
    grades.entity_name_with_location as entity_name_with_location,
    grades.actor_id as actor_id,
    grades.grade_type as grade_type,
    grades.scaled_score as scaled_score,
    grades.grade_bucket as grade_bucket
from
    grades
    join most_recent_grades
        using (org, course_key, entity_id, actor_id, emission_time)
