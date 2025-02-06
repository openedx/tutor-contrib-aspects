with
    latest_emission_time as (
        select org, course_key, actor_id, MAX(emission_time) as last_visited
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_course_visit
        where
            1 = 1
            {% include 'openedx-assets/queries/common_filters.sql' %}
            {% include 'openedx-assets/queries/user_filters.sql' %}
        group by org, course_key, actor_id
    ),
    enrollment_status as (
        select org, course_key, actor_id, MAX(emission_time) as max_emission_time
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_enrollment
        where
            1 = 1
            {% include 'openedx-assets/queries/common_filters.sql' %}
            {% include 'openedx-assets/queries/user_filters.sql' %}
        group by org, course_key, actor_id
    ),
    student_status as (
        select
            fss.org as org,
            fss.course_key as course_key,
            fss.actor_id as actor_id,
            fss.course_name as course_name,
            fss.course_run as course_run,
            fss.approving_state as approving_state,
            fss.enrollment_mode as enrollment_mode,
            fss.enrollment_status as enrollment_status,
            fss.course_grade as course_grade,
            fss.grade_bucket as grade_bucket,
            fss.username as username,
            fss.name as name,
            fss.email as email,
            fss.enrolled_at as enrolled_at
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status fss
        where
            1 = 1
            {% include 'openedx-assets/queries/common_filters.sql' %}
            {% include 'openedx-assets/queries/user_filters.sql' %}
    )
select
    fss.org as org,
    fss.course_key as course_key,
    fss.actor_id as actor_id,
    fss.course_name as course_name,
    fss.course_run as course_run,
    fss.approving_state as approving_state,
    fss.enrollment_mode as enrollment_mode,
    fss.enrollment_status as enrollment_status,
    fss.course_grade as course_grade,
    fss.grade_bucket as grade_bucket,
    fss.username as username,
    fss.name as name,
    fss.email as email,
    fes.max_emission_time as emission_time,
    GREATEST(let.last_visited, fss.enrolled_at) as last_visited
from student_status fss
left join
    enrollment_status fes
    on fss.org = fes.org
    and fss.course_key = fes.course_key
    and fss.actor_id = fes.actor_id
left join
    latest_emission_time let
    on fss.org = let.org
    and fss.course_key = let.course_key
    and fss.actor_id = let.actor_id
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
