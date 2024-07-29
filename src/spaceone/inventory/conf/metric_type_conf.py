
METRIC_TYPE = {
    'VM_Instance': [
        {'key': 'CPU_Utilization', 'value': 'compute.googleapis.com/instance/cpu/utilization'},
        {'key': 'Memory_Utilization', 'value': 'agent.googleapis.com/memory/percent_used'},
        {'key': 'Disk_Space_Utilization', 'value': 'agent.googleapis.com/disk/percent_used'}
    ],
    'Compute_Disk': [
        {'key': 'Read_IOPS', 'value': 'compute.googleapis.com/instance/disk/read_ops_count'},
        {'key': 'Write_IOPS', 'value': 'compute.googleapis.com/instance/disk/write_ops_count'}
    ],
    'SQL_Instance': [
        {'key': 'CPU_Utilization', 'value': 'cloudsql.googleapis.com/database/cpu/utilization'},
        {'key': 'Memory_Utilization', 'value': 'cloudsql.googleapis.com/database/memory/utilization'},
        {'key': 'Disk_Space_Utilization', 'value': 'cloudsql.googleapis.com/database/disk/utilization'}
    ]
}
