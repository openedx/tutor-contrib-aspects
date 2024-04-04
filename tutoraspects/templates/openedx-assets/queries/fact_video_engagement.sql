with
    subsection_counts as (
        select
            org,
            course_key,
            section_with_name,
            subsection_with_name,
            actor_id,
            item_count,
            countDistinct(video_id) as videos_viewed,
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
            {% if from_dttm is not none %}
                and viewed_on > date('{{ from_dttm }}')
            {% endif %}
            {% if to_dttm is not none %}
                and viewed_on < date('{{ to_dttm }}')
            {% endif %}
            {% endraw %}
            {% include 'openedx-assets/queries/common_filters.sql' %}
        group by
            org,
            course_key,
            section_with_name,
            subsection_with_name,
            actor_id,
            item_count
    ),
    section_counts as (
        select
            org,
            course_key,
            section_with_name,
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
        group by org, course_key, section_with_name, actor_id
    )

select
    org,
    course_key,
    subsection_with_name as `section/subsection name`,
    'subsection' as `content level`,
    actor_id as actor_id,
    engagement_level as `section/subsection video engagement`
from subsection_counts
union all
select
    org,
    course_key,
    section_with_name as `section/subsection name`,
    'section' as `content level`,
    actor_id as actor_id,
    engagement_level as `section/subsection video engagement`
from section_counts
