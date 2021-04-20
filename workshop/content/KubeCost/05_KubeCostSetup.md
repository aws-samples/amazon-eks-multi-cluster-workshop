---
title: "Install and Configure KubeCost"
weight: 5 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

In this lab, we'll setup a kubecost and configure our clusters for monitoring.

## Prometheus

Kubecost uses Prometheus for metric collection.
If you have already installed Prometheus from the previous section, you can skip this part.
If not run the below commands to install the Prometheus Helm chart, and install Prometheus in the cluster. 

    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm install prometheus prometheus-community/prometheus \
        --namespace prometheus \
        --set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2",server.service.type=LoadBalancer


## KubeCost

With Prometheus installed, the next step is to clone the KubeCost repository.

    cd ~
    git clone https://github.com/kubecost/cost-model.git
    cd cost-model/

Before we install KubeCost we need to update the configuration file to point to our Prometheus installation.
Note that we are using the default Prometheus service name.
If you changed the Prometheus endpoint name as part of your installation make sure to update it below.


    prometheusEndpoint='http://prometheus-server.prometheus.svc.cluster.local'
    sed -i "s|{{prometheusEndpoint}}|$prometheusEndpoint|" kubernetes/deployment.yaml

    kubectl create namespace cost-model
    kubectl apply -f kubernetes/ --namespace cost-model

### Update Prometheus Job

The last step is to update our Prometheus config to scrape metrics from KubeCost.
First get the latest Prometheus configuration.

    cd ~
    kubectl get configmap prometheus-server --namespace=prometheus  -o yaml > prometheus-server.yaml

Next open up the configuration in your editor of choice.

    nano prometheus-server.yaml

Add the following job to the Prometheus config in the jobs section.
Also be sure to update the cost model target if you changed it from the default.

```yaml
    - job_name: kubecost
      honor_labels: true
      scrape_interval: 1m
      scrape_timeout: 10s
      metrics_path: /metrics
      scheme: http
      static_configs:
      - targets:
        - cost-model.cost-model.svc.cluster.local:9003
```
Finally reapply the configuration file.

    kubectl apply -f prometheus-server.yaml 

### Reload Prometheus

With our new job in place, the last step is to reload Prometheus to start the new collection job.

    prometheusLB=$(kubectl get svc --namespace prometheus prometheus-server -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    curl -X POST $prometheusLB/-/reload



Continue to the next section. 
