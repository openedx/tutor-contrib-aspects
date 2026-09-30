select
    l.dttm as action_date,
    case
        when LOWER(l.action) = 'queries'
        then 'query from sqllab'
        when LOWER(l.action) = 'chartrestapi.data'
        then 'query from charts'
        when LOWER(l.action) = 'count'
        then 'dashboard view'
        when LOWER(l.action) like 'annotation%'
        then 'annotations'
        when LOWER(l.action) like 'css%'
        then 'CSS'
        else LOWER(l.action)
    end as action,
    l.user_id,
    u.username as user_name,
    u.created_on as user_registration_date,
    l.dashboard_id,
    d.dashboard_title,
    case when d.published = TRUE then 'published' else 'draft' end as dashboard_status,
    l.slice_id,
    s.slice_name,
    s.datasource_type,
    s.datasource_name,
    s.datasource_id,
    COUNT(1) as action_count
from logs as l
left join ab_user as u on u.id = l.user_id
left join dashboards as d on d.id = l.dashboard_id
left join slices as s on s.id = l.slice_id
where 1 = 1 and l.action != 'log'
group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
