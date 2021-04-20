---
title: "First Pipeline"
date: 2020-04-28T10:16:11-06:00
weight: 15
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

1.	Connect to Spinnaker using Spinnaker URL. Your browser window should look like this

![](/images/spinnaker/eks_spinnaker.png)
 
2.	From actions menu (top right part of Spinnaker Web UI) select Create Application and provide application name as eks-multi also provide an email address you want to assign to application. Other options are not required. 
![](/images/spinnaker/eks_create_application.png)
 
3.	Click on Create. 

Once Application is created you can start building your deployment pipeline.

1.	From Pipeline section select “Configure new pipeline” and name it “multi-pipeline”
![](/images/spinnaker/eks_create_new_pipeline_1.png)
 
 
2.	Deployment pipeline will consist of 2 steps 
*	Initial deployment to first EKS Cluster
*	Manual judgement step to verify successful deployment.

3.	Once initial (empty) pipeline is created start by creating first step
4.	Click on “Add stage” and choose “Deploy Manifest” as Type, and select “eks-cluster-1” as account for manifest deployment in Basic Settings.
![](/images/spinnaker/eks_deploy_manifest.png)
 
5.	Paste following kubernetes manifest in “Manifest configuration” 

```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  annotations:
    strategy.spinnaker.io/max-version-history: '2'
    traffic.spinnaker.io/load-balancers: '["service lb-aws1"]'
  labels:
    app: app-aws1
  name: app-aws1-frontend
spec:
  replicas: 1
  selector:
    matchLabels:
     app: app-aws
  template:
    metadata:
     labels:
      app: app-aws
    spec:
       containers:
         - image: index.docker.io/mbednarz/multi-eks
           name: frontend
```
●	Click “Add Stage” to include “Manual Judgement” step
![](/images/spinnaker/eks_manual_judgement.png)


