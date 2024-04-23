with
    subsection_counts as (
        select
            org,
            course_key,
            course_run,
            section_with_name,
            subsection_with_name,
            actor_id,
            page_count,
            count(distinct block_id) as pages_visited,
            case
                when pages_visited = 0
                then 'No pages viewed yet'
                when pages_visited = page_count
                then 'All pages viewed'
                else 'At least one page viewed'
            end as engagement_level
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_navigation_completion
        where
            1 = 1
            {% raw %}
            {% if from_dttm %} and visited_on > date('{{ from_dttm }}') {% endif %}
            {% if to_dttm %} and visited_on < date('{{ to_dttm }}') {% endif %}
            {% endraw %}
            {% include 'openedx-assets/queries/common_filters.sql' %}
        group by
            org,
            course_key,
            course_run,
            section_with_name,
            subsection_with_name,
            actor_id,
            page_count
    ),
    section_counts as (
        select
            org,
            course_key,
            course_run,
            section_with_name,
            '' as subsection_with_name,
            actor_id,
            sum(page_count) as page_count,
            sum(pages_visited) as pages_visited,
            case
                when pages_visited = 0
                then 'No pages viewed yet'
                when pages_visited = page_count
                then 'All pages viewed'
                else 'At least one page viewed'
            end as engagement_level
        from subsection_counts
        group by
            org,
            course_key,
            course_run,
            section_with_name,
            subsection_with_name,
            actor_id
    )

select
    org,
    course_key,
    course_run,
    section_with_name as section_with_name,
    subsection_with_name as subsection_with_name,
    subsection_with_name as `section/subsection name`,
    'subsection' as `content level`,
    actor_id as actor_id,
    engagement_level as `section/subsection page engagement`
from subsection_counts
union all
select
    org,
    course_key,
    course_run,
    section_with_name as section_with_name,
    subsection_with_name as subsection_with_name,
    section_with_name as `section/subsection name`,
    'section' as `content level`,
    actor_id as actor_id,
    engagement_level as `section/subsection page engagement`
from section_counts
