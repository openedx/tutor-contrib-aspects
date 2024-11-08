"""Filters usage."""

from tutorpod_autoscaling.hooks import (  # pylint: disable=import-error
    AUTOSCALING_CONFIG,
)


@AUTOSCALING_CONFIG.add()
def add_aspects_autoscaling(autoscaling_config):
    """Add autoscaling values for Aspects services."""
    autoscaling_config.update(
        {
            "ralph": {
                "enable_hpa": True,
                "memory_request": "300Mi",
                "cpu_request": 0.25,
                "memory_limit": "600Mi",
                "cpu_limit": 1,
                "min_replicas": 1,
                "max_replicas": 10,
                "avg_cpu": 80,
                "avg_memory": "",
                "enable_vpa": False,
            },
            "superset": {
                "enable_hpa": True,
                "memory_request": "500Mi",
                "cpu_request": 0.25,
                "memory_limit": "1000Mi",
                "cpu_limit": 1,
                "min_replicas": 1,
                "max_replicas": 10,
                "avg_cpu": 80,
                "avg_memory": "",
                "enable_vpa": False,
            },
            "superset-worker": {
                "enable_hpa": True,
                "memory_request": "600Mi",
                "cpu_request": 0.25,
                "memory_limit": "1500Mi",
                "cpu_limit": 1,
                "min_replicas": 1,
                "max_replicas": 10,
                "avg_cpu": 80,
                "avg_memory": "",
                "enable_vpa": False,
            },
        }
    )
    return autoscaling_config
