with
    subsection_engagement as (
        select
            org,
            course_key,
            'subsection' as content_level,
            actor_id,
            subsection_block_id as block_id,
            engagement_level as section_subsection_page_engagement
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_subsection_page_engagement
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    ),
    section_engagement as (
        select
            org,
            course_key,
            'section' as content_level,
            actor_id,
            section_block_id as block_id,
            engagement_level as section_subsection_page_engagement
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_section_page_engagement
    ),
    page_engagement as (
        select *
        from subsection_engagement
        union all
        select *
        from section_engagement
    )

select
    pv.org as org,
    pv.course_key as course_key,
    course_blocks.course_run as course_run,
    course_blocks.display_name_with_location as section_subsection_name,
    pv.content_level as content_level,
    pv.actor_id as actor_id,
    pv.section_subsection_page_engagement as section_subsection_page_engagement,
    users.username as username,
    users.name as name,
    users.email as email
from page_engagement pv
join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks course_blocks
    on (
        pv.org = course_blocks.org
        and pv.course_key = course_blocks.course_key
        and pv.block_id = course_blocks.block_id
    )
left outer join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_user_pii users
    on (pv.actor_id like 'mailto:%' and SUBSTRING(pv.actor_id, 8) = users.email)
    or pv.actor_id = toString(users.external_user_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
