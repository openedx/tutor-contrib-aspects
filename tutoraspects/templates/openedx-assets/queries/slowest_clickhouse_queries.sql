SELECT
    event_time,
    query_duration_ms / 1000 AS duration_secs,
    read_rows,
    memory_usage / 1024 AS memory_usage_kb,
    query
FROM
    system.query_log
WHERE
    type = 'QueryFinish'
ORDER BY
    query_duration_ms DESC;
