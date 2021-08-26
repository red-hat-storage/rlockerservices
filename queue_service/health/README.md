# Use this directory as a location of the health status of the service

## This directory will include logs regarding the health status of the queue_service

You can benefit from this folder by adding `livenessprobe`, `readinessprobe` conditionals whenever you use this platform in a K8 / OCP Cluster.

### Please check which condition the service checks in the ____exit____ method in [this file](../queue_service/queue_service.py)