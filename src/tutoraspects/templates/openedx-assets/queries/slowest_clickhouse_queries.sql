select
    event_time,
    query_duration_ms / 1000 as duration_secs,
    read_rows,
    memory_usage / 1024 as memory_usage_kb,
    query
from system.query_log
where type = 'QueryFinish'
order by query_duration_ms DESC
;
