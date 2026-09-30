select name, toFloat64(value) as value, description
from system.metrics
where metric in ('Query', 'DelayedInserts', 'DistributedFilesToInsert')

union all

select metric as name, round(toFloat64(value), 2) as value, description
from system.asynchronous_metrics
where metric in ('MaxPartCountForPartition', 'Uptime')

union all

select name, toFloat64(value) as value, description
from system.events
where
    event in (
        'RejectedInserts',
        'ReplicatedDataLoss',
        'DataAfterMergeDiffersFromReplica',
        'DataAfterMutationDiffersFromReplica'
    )

union all

select
    'StuckReplicationTasks' as name,
    toFloat64(count()) as value,
    'Replication tasks that were retried or postponed over 100 times.' as description
from system.replication_queue
where num_tries > 100 or num_postponed > 100

union all

select
    CONCAT('cluster ', name) as name,
    ROUND(SUM(free_space) / SUM(total_space), 3) * 100 as value,
    'Free space per cluster node, as percent' as description
from system.disks
group by name
