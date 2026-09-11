with
    most_recent as (
        select
            id,
            multiIf(parent = 0, id, CAST(parent, 'int')) as sort_order_1,
            multiIf(parent = 0, 0, 1) as sort_order_2,
            concat(repeat('- ', countMatches(lineage, ',')), value) as tag,
            row_number() over (
                order by sort_order_1 ASC, sort_order_2 ASC, value ASC
            ) as rownum
        from {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_most_recent_tags
    )
select
    most_recent.id as tag_id,
    most_recent.rownum as rownum,
    most_recent.tag as tag,
    tags.course_key as course_key
from most_recent
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_course_tags tags
    on tags.tag_id = most_recent.id
