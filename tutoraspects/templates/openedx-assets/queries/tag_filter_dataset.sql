with
    data as (
        select
            id,
            case when parent = 0 then id else cast(parent as int) end as sort_order_1,
            case when parent = 0 then 0 else 1 end as sort_order_2,
            concat(repeat('- ', countMatches(lineage, ',')), value) as tag,
            row_number() over (order by sort_order_1, sort_order_2, value) as rownum
        from {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_tags
    )
select id, rownum, tag
from data
