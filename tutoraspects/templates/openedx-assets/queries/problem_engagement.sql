with
    subsection_engagement as (
        select
            org,
            course_key,
            'subsection' as content_level,
            actor_id,
            subsection_block_id as block_id,
            engagement_level as section_subsection_problem_engagement
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_subsection_problem_engagement
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}

    ),
    section_engagement as (
        select
            org,
            course_key,
            'section' as content_level,
            actor_id,
            section_block_id as block_id,
            engagement_level as section_subsection_problem_engagement
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_section_problem_engagement
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    ),
    problem_engagement as (
        select *
        from subsection_engagement
        union all
        select *
        from section_engagement
    )
select
    pe.org as org,
    pe.course_key as course_key,
    course_blocks.course_run as course_run,
    course_blocks.display_name_with_location as section_subsection_name,
    pe.content_level as content_level,
    pe.actor_id as actor_id,
    pe.section_subsection_problem_engagement as section_subsection_problem_engagement,
    users.username as username,
    users.name as name,
    users.email as email
from problem_engagement pe
join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks course_blocks
    on (
        pe.org = course_blocks.org
        and pe.course_key = course_blocks.course_key
        and pe.block_id = course_blocks.block_id
    )
left outer join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_user_pii users
    on (pe.actor_id like 'mailto:%' and SUBSTRING(pe.actor_id, 8) = users.email)
    or pe.actor_id = toString(users.external_user_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
