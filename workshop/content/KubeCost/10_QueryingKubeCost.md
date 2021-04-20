---
title: "Querying KubeCost"
weight: 10 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

In this lab, we will use Prometheus and KubeCost to gain insight into the cost of our cluster.

## Prometheus

We will be running all of our queries from the Prometheus UI.
Run the below command to get the the Prometheus endpoint.
Open this URL in your browser. 

        kubectl get svc --namespace prometheus prometheus-server -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

## Sample Queries

All of these sample queries can be run from the main Prometheus UI. 
After you place the query in the expression box, press execute button to see the results.

![Prometheus UI](/images/kubecost/prometheus.png)


### Monthly Cost of Top 10 Containers

    topk( 10, 
        container_memory_allocation_bytes* on(instance) group_left() node_ram_hourly_cost  / 1024 / 1024 / 1024 * 730
        + 
        container_cpu_allocation * on(instance) group_left() node_cpu_hourly_cost * 730
    )

### Monthly Namespace Cost

    sum(
        container_cpu_allocation * on (node) group_left node_cpu_hourly_cost 
        +
        container_memory_allocation_bytes* on (node) group_left() node_ram_hourly_cost  / 1024 / 1024 / 1024 
    ) by (namespace) * 720

### Monthly Node Cost

    sum(node_total_hourly_cost) * 730

### Monthly LoadBalancer Cost

    sum(kubecost_load_balancer_cost) * 730

## Available Metrics

Below is a full list of the current metrics currently available in Kubecost. 

| Metric       | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| node_cpu_hourly_cost | Hourly cost per vCPU on this node  |
| node_gpu_hourly_cost | Hourly cost per GPU on this node  |
| node_ram_hourly_cost   | Hourly cost per Gb of memory on this node                       |
| node_total_hourly_cost   | Total node cost per hour                       |
| kubecost_load_balancer_cost   | Hourly cost of a load balancer                 |
| kubecost_cluster_management_cost | Hourly management fee per cluster                 |
| pv_hourly_cost   | Hourly cost per GP on a persistent volume                 |
| container_cpu_allocation   | Average number of CPUs requested/used over last 1m                      |
| container_gpu_allocation   | Average number of GPUs requested over last 1m                      |
| container_memory_allocation_bytes   | Average bytes of RAM requested/used over last 1m                 |
| pod_pvc_allocation   | Bytes provisioned for a PVC attached to a pod                      |
