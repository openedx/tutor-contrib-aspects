with
    subsection_counts as (
        select
            org,
            course_key,
            course_run,
            section_with_name,
            subsection_with_name,
            actor_id,
            item_count,
            count(distinct problem_id) as problems_attempted,
            case
                when problems_attempted = 0
                then 'No problems attempted yet'
                when problems_attempted = item_count
                then 'All problems attempted'
                else 'At least one problem attempted'
            end as engagement_level,
            username,
            name,
            email
        from {{ ref("fact_problem_engagement_per_subsection") }}
        group by
            org,
            course_key,
            course_run,
            section_with_name,
            subsection_with_name,
            actor_id,
            item_count,
            username,
            name,
            email
        where 1=1
            {% include 'openedx-assets/queries/common_filters.sql' %}
    ),
    section_counts as (
        select
            org,
            course_key,
            course_run,
            section_with_name,
            actor_id,
            sum(item_count) as item_count,
            sum(problems_attempted) as problems_attempted,
            case
                when problems_attempted = 0
                then 'No problems attempted yet'
                when problems_attempted = item_count
                then 'All problems attempted'
                else 'At least one problem attempted'
            end as engagement_level,
            username,
            name,
            email
        from subsection_counts
        where 1=1
            {% include 'openedx-assets/queries/common_filters.sql' %}
        group by
            org,
            course_key,
            course_run,
            section_with_name,
            actor_id,
            username,
            name,
            email
    ),
    problem_engagement as (
        select
            org,
            course_key,
            course_run,
            subsection_with_name as section_subsection_name,
            'subsection' as content_level,
            actor_id as actor_id,
            engagement_level as section_subsection_problem_engagement,
            username,
            name,
            email
        from subsection_counts
        union all
        select
            org,
            course_key,
            course_run,
            section_with_name as section_subsection_name,
            'section' as content_level,
            actor_id as actor_id,
            engagement_level as section_subsection_problem_engagement,
            username,
            name,
            email
        from section_counts
    )

select
    pe.org as org,
    pe.course_key as course_key,
    pe.course_run as course_run,
    pe.section_subsection_name as section_subsection_name,
    pe.content_level as content_level,
    pe.actor_id as actor_id,
    pe.section_subsection_problem_engagement as section_subsection_problem_engagement,
    pe.username as username,
    pe.name as name,
    pe.email as email
from problem_engagement pe
