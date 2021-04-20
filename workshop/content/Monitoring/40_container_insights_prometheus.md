---
title: "(OPTIONAL) Container Insights with Prometheus"
date: 2020-04-28T10:16:11-06:00
weight: 40 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0


To install the CloudWatch agent with Prometheus support on an Amazon EKS cluster

Enter the following command to check whether the amazon-cloudwatch namespace has already been created:

```
kubectl get namespace
```

If amazon-cloudwatch is not displayed in the results, create it by entering the following command:

````
kubectl create namespace amazon-cloudwatch
````

To deploy the agent with the default configuration and have it send data to the AWS Region that it is installed in, enter the following command:
Note

The following setup step pulls the container image from Docker Hub as an anonymous user by default. This pull may be subject to a rate limit. For more information, see Container Image and Download Rate Limit.

```
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/master/k8s-deployment-manifest-templates/deployment-mode/service/cwagent-prometheus/prometheus-eks.yaml
```
To have the agent send data to a different Region instead, follow these steps:

Download the YAML file for the agent by entering the following command:
```
curl -O https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/master/k8s-deployment-manifest-templates/deployment-mode/service/cwagent-prometheus/prometheus-eks.yaml
```
Open the file with a text editor, and search for the cwagentconfig.json block of the file.

Add the highlighted lines, specifying the Region that you want:

```
cwagentconfig.json: |
    {
      "agent": {
        "region": "us-east-2"
      },
      "logs": { ...
```
Save the file and deploy the agent using your updated file.

```
kubectl apply -f prometheus-eks.yaml
```
