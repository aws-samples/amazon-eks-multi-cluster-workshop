---
title: "Single pane EKS monitoring with Container Insights"
date: 2020-04-28T10:16:11-06:00
weight: 30 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

To deploy Container Insights review the following command: 

```
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/cluster-name/;s/{{region_name}}/cluster-region/" | kubectl apply -f -
```
In this command, cluster-name is the name of your Amazon EKS cluster and cluster-region is the name of the Region where the logs are published. We recommend that you use the same Region where your cluster is deployed to reduce the AWS outbound data transfer costs. 

In order to deploy Container Insights for our first cluster in current region please execute following command in Cloud9 environment: 

```
kubectl config use-context cluster1
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/$CLUSTER1_NAME/;s/{{region_name}}/$AWS_REGION/" | kubectl apply -f -
```

To deploy Container Insights for eks-cluster-2, run: 

```
kubectl config use-context cluster2
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/$CLUSTER2_NAME/;s/{{region_name}}/$AWS_REGION/" | kubectl apply -f -
```

Navigate to CloudWatch and open Container Insights. After several minutes you should be able to see metrics, and logs coming from all registered clusters.

![](/images/spinnaker/eks_container_insights.png)
