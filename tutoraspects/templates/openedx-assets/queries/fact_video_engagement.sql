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
            count(distinct video_id) as videos_viewed,
            case
                when videos_viewed = 0
                then 'No videos viewed yet'
                when videos_viewed = item_count
                then 'All videos viewed'
                else 'At least one video viewed'
            end as engagement_level
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_engagement
        where
            1 = 1
            {% raw %}
            {% if from_dttm %} and viewed_on > date('{{ from_dttm }}') {% endif %}
            {% if to_dttm %} and viewed_on < date('{{ to_dttm }}') {% endif %}
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
            '' as subsection_with_name,
            actor_id,
            sum(item_count) as item_count,
            sum(videos_viewed) as videos_viewed,
            case
                when videos_viewed = 0
                then 'No videos viewed yet'
                when videos_viewed = item_count
                then 'All videos viewed'
                else 'At least one video viewed'
            end as engagement_level
        from subsection_counts
        group by
            org,
            course_key,
            course_run,
            section_with_name,
            subsection_with_name,
            actor_id
    ),
    all_counts as (

        select
            org,
            course_key,
            course_run,
            section_with_name as section_with_name,
            subsection_with_name as subsection_with_name,
            subsection_with_name as `section/subsection name`,
            'subsection' as `content level`,
            actor_id as actor_id,
            engagement_level as `section/subsection video engagement`
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
            engagement_level as `section/subsection video engagement`
        from section_counts
    )
select *
from all_counts
where
    1 = 1
    {% raw %}
    {% if filter_values("Section Name") != [] %}
        and section_with_name in {{ filter_values("Section Name") | where_in }}
    {% endif %}
    {% if filter_values("Subsection Name") != [] %}
        and subsection_with_name in {{ filter_values("Subsection Name") | where_in }}
    {% endif %}
    {% endraw %}
