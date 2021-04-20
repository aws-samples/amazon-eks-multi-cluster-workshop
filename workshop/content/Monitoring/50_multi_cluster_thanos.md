---
title: "Multi-cluster monitoring with Prometheus and Thanos"
date: 2020-04-28T10:16:11-06:00
weight: 50 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

Prometheus is an open source systems monitoring and alerting toolkit that is widely adopted as a standard monitoring tool with self-managed and provider-managed Kubernetes. Prometheus provides many useful features, such as dynamic service discovery, powerful queries, and seamless alert notification integration. Beyond certain scale, however, problems arise when basic Prometheus capabilities do not meet requirements such as:

*    Storing petabyte-scale historical data in a reliable and cost-efficient way
*    Accessing all metrics using a single-query API
*    Merging replicated data collected via Prometheus high-availability (HA) setups

Thanos was built in response to these challenges. Thanos, which is released under the Apache 2.0 license, offers a set of components that can be composed into a highly available Prometheus setup with long-term storage capabilities. Thanos uses the Prometheus 2.0 storage format to cost-efficiently store historical metric data in object storage, such as Amazon Simple Storage Service (Amazon S3), while retaining fast query latencies. In summary, Thanos is intended to provide:

*    Global query view of metrics
*    Virtually unlimited retention of metrics, including downsampling
*    High availability of components, including support for Prometheus HA


![](/images/spinnaker/eks_thanos.png)


Start by creating a new EKS cluster for Thanos (cluster3).

```bash
cd ~/environment/eks-multi/
cdk deploy EksMulti-eks-c3
```

Update environment variables for cluster3 

```bash
source ~/environment/eks-multi/scripts/update-kube-config-thanos.sh 
```


{{% notice note %}}
Make sure  to delete existing prometheus/grafana deployment from your clusters by executing following commands : 
{{% /notice %}}

```bash
kubectl config use-context cluster1
helm uninstall grafana --namespace grafana 
helm uninstall prometheus --namespace prometheus

kubectl config use-context cluster2
helm uninstall grafana --namespace grafana 
helm uninstall prometheus --namespace prometheus
```

Add Bitnami Helm charts repo:

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```


Install Prometheus with Thanos sidecar on first cluster:

```bash
kubectl config use-context cluster1
helm install prometheus bitnami/kube-prometheus --set prometheus.thanos.create=true \
   --set operator.service.type=ClusterIP \
   --set prometheus.service.type=ClusterIP \
   --set alertmanager.service.type=ClusterIP \
   --set prometheus.thanos.service.type=LoadBalancer \
   --set prometheus.externalLabels.cluster="data-producer-1"
```

Set environmental variable for Thanos endpoint on first cluster:
```bash
export THANOS_1=$(kubectl get service prometheus-kube-prometheus-prometheus-thanos -o json | jq -r '.status.loadBalancer.ingress[].hostname')
```

Proceed with similar procedure on the seconds cluster:

```bash
kubectl config use-context cluster2
helm install prometheus bitnami/kube-prometheus --set prometheus.thanos.create=true \
   --set operator.service.type=ClusterIP \
   --set prometheus.service.type=ClusterIP \
   --set alertmanager.service.type=ClusterIP \
   --set prometheus.thanos.service.type=LoadBalancer \
   --set prometheus.externalLabels.cluster="data-producer-2"
```
Set environmental variable for Thanos endpoint on second cluster:
```bash
export THANOS_2=$(kubectl get service prometheus-kube-prometheus-prometheus-thanos -o json | jq -r '.status.loadBalancer.ingress[].hostname')
```

Update helm values for Thanos observer instance and deploy Thanos observer

```bash
kubectl config use-context cluster3
cat ~/environment/eks-multi/scripts/values.yaml | sed "s/{{thanos_bucket}}/$THANOS_BUCKET/;s/{{thanos_1}}/$THANOS_1/;s/{{thanos_2}}/$THANOS_2/;s/{{region_name}}/$AWS_REGION/" > /tmp/thanos-values.yaml
helm install thanos bitnami/thanos --values /tmp/thanos-values.yaml
```

Deploy Grafana 

```bash
kubectl create namespace grafana
helm install grafana grafana/grafana \
    --namespace grafana \
    --set persistence.storageClassName="gp2" \
    --set persistence.enabled=true \
    --set adminPassword='AWSomePassword' \
    --set datasources."datasources\.yaml".apiVersion=1 \
    --set datasources."datasources\.yaml".datasources[0].name=Thanos \
    --set datasources."datasources\.yaml".datasources[0].type=prometheus \
    --set datasources."datasources\.yaml".datasources[0].url=http://thanos-query.default.svc.cluster.local:9090 \
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

Create the dashboard to monitor multiple clusters with Thanos:

    Click '+' button on left panel and select ‘Import’.
    Enter 14051 dashboard id under Grafana.com Dashboard.
    Click ‘Load’.
    Select ‘Thanos’ as the endpoint under Thanos data sources drop down.
    Click ‘Import’.

You now have a single dashboard to access metrics from all EKS clusters using Thanos.

Cleanup 

```
kubectl config use-context cluster1
helm uninstall prometheus
kubectl config use-context cluster2
helm uninstall prometheus
kubectl config use-context cluster3
helm uninstall thanos
```
