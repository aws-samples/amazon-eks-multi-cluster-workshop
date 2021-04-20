---
title: "Prometheus deployment"
date: 2020-04-28T10:16:11-06:00
weight: 20 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

We will use a Prometheus stable Helm chart to deploy monitoring stack on for both clusters.
In order to do so you need to :

* Start by adding Prometheus and Grafana Helm chart repositories

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
```

* Install Prometheus on a first Cluster

```
kubectl config use-context cluster1
kubectl create namespace prometheus
helm install prometheus prometheus-community/prometheus \
             --namespace prometheus \
             --set alertmanager.persistentVolume.storageClass="gp2",server.persistentVolume.storageClass="gp2",server.service.type=LoadBalancer
```

Take note of the load balancer URL and navigate to Prometheus to verify it is running and collecting the metrics.
```
kubectl get svc --namespace prometheus prometheus-server -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'; echo
```

Install Grafana for Prometheus visualization

```
kubectl create namespace grafana
helm install grafana grafana/grafana \
    --namespace grafana \
    --set persistence.storageClassName="gp2" \
    --set persistence.enabled=true \
    --set adminPassword='AWSomePassword' \
    --set datasources."datasources\.yaml".apiVersion=1 \
    --set datasources."datasources\.yaml".datasources[0].name=Prometheus \
    --set datasources."datasources\.yaml".datasources[0].type=prometheus \
    --set datasources."datasources\.yaml".datasources[0].url=http://prometheus-server.prometheus.svc.cluster.local \
    --set datasources."datasources\.yaml".datasources[0].access=proxy \
    --set datasources."datasources\.yaml".datasources[0].isDefault=true \
    --set dashboardProviders."dashboardproviders\.yaml".apiVersion=1 \
    --set dashboardProviders."dashboardproviders\.yaml".providers[0].name=default \
    --set dashboardProviders."dashboardproviders\.yaml".providers[0].orgId=1 \
    --set dashboardProviders."dashboardproviders\.yaml".providers[0].folder="" \
    --set dashboardProviders."dashboardproviders\.yaml".providers[0].type=file \
    --set dashboardProviders."dashboardproviders\.yaml".providers[0].disableDeletion=false \
    --set dashboardProviders."dashboardproviders\.yaml".providers[0].editable=true \
    --set dashboardProviders."dashboardproviders\.yaml".providers[0].options.path=/var/lib/grafana/dashboards/default \
    --set service.type=LoadBalancer
```

Verify Grafana load balancer URL by executing 

```
kubectl get svc --namespace grafana grafana -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'; echo
```

Navigate to Grafana load balancer URL and use admin/AWSomePassword credentials to authenticate and verify operations.

Cluster Monitoring Dashboard

For creating a dashboard to monitor the cluster:

    Click '+' button on left panel and select ‘Import’.
    Enter 3119 dashboard id under Grafana.com Dashboard.
    Click ‘Load’.
    Select ‘Prometheus’ as the endpoint under prometheus data sources drop down.
    Click ‘Import’.


 
To deploy Prometheus and Grafana on the second EKS cluster.
Follow the same instructions as above, but using the context for the second cluster:

    kubectl config use-context cluster2


The Cloud Native Computing Foundation’s Prometheus project is a popular open source monitoring and alerting solution optimized for container environments. .
This approach allows you to use Prometheus and Grafana deployed independently on your EKS clusters.

Uninstall Grafana and Prometheus 

```bash

kubectl config use-context cluster1
helm uninstall grafana --namespace grafana 
helm uninstall prometheus --namespace prometheus

kubectl config use-context cluster2
helm uninstall grafana --namespace grafana 
helm uninstall prometheus --namespace prometheus
```
