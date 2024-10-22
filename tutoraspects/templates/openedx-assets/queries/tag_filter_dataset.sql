SELECT id, rownum, tag, course_key
FROM (
    SELECT 
        id, 
        multiIf(parent = 0, id, CAST(parent, 'int')) AS sort_order_1, 
        multiIf(parent = 0, 0, 1) AS sort_order_2, 
        concat(repeat('- ', countMatches(lineage, ',')), value) AS tag, 
        row_number() OVER (ORDER BY sort_order_1 ASC, sort_order_2 ASC, value ASC) AS rownum 
    FROM {{ ASPECTS_EVENT_SINK_DATABASE }}.most_recent_tags
) as t
left join {{ DBT_PROFILE_TARGET_DATABASE }}.most_recent_course_tags ct on ct.tag_id = t.id
