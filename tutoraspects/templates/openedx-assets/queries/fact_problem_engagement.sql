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
            end as engagement_level
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_problem_engagement
        where
            1 = 1
            {% raw %}
            {% if from_dttm %}
                and attempted_on > date('{{ from_dttm }}')
            {% endif %}
            {% if to_dttm %}
                and attempted_on < date('{{ to_dttm }}')
            {% endif %}
            {% endraw %}
            {% include 'openedx-assets/queries/common_filters.sql' %}
        group by
            org,
            course_key,
            course_run,
            section_with_name,
            subsection_with_name,
            actor_id,
            item_count
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
            end as engagement_level
        from subsection_counts
        group by org, course_key, course_run, section_with_name, actor_id
    )

select
    org,
    course_key,
    course_run,
    subsection_with_name as `section/subsection name`,
    'subsection' as `content level`,
    actor_id as actor_id,
    engagement_level as `section/subsection problem engagement`
from subsection_counts
union all
select
    org,
    course_key,
    course_run,
    section_with_name as `section/subsection name`,
    'section' as `content level`,
    actor_id as actor_id,
    engagement_level as `section/subsection problem engagement`
from section_counts
