SELECT
    l.dttm AS action_date,
    CASE
        WHEN LOWER(
            l.action
        ) = 'queries' THEN 'query from sqllab'
        WHEN LOWER(
            l.action
        ) = 'chartrestapi.data' THEN 'query from charts'
        WHEN LOWER(
            l.action
        ) = 'count' THEN 'dashboard view'
        WHEN LOWER(
            l.action
        ) LIKE 'annotation%' THEN 'annotations'
        WHEN LOWER(
            l.action
        ) LIKE 'css%' THEN 'CSS'
        ELSE LOWER(
            l.action
        )
    END AS action,
    l.user_id,
    u.username AS user_name,
    u.created_on AS user_registration_date,
    l.dashboard_id,
    d.dashboard_title,
    CASE
        WHEN d.published = TRUE THEN 'published'
        ELSE 'draft'
    END AS dashboard_status,
    l.slice_id,
    s.slice_name,
    s.datasource_type,
    s.datasource_name,
    s.datasource_id,
    COUNT(1) AS action_count
FROM
    logs AS l
    LEFT JOIN ab_user AS u
    ON u.id = l.user_id
    LEFT JOIN dashboards AS d
    ON d.id = l.dashboard_id
    LEFT JOIN slices AS s
    ON s.id = l.slice_id
WHERE
    1 = 1
    AND l.action != 'log'
GROUP BY
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13
