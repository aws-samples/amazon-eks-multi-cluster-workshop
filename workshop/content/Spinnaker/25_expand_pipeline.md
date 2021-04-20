---
title: "Multi-cluster Pipeline"
date: 2020-04-28T10:16:11-06:00
weight: 25
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

Now it's time to extend our pipeline across multiple cluster. This approach allows to deploy workloads simultaneously across multiple clusters
or follow sequential deployment patterns. Our extended pipeline will use the second approach and deploy to eks-cluster-1 and after manual acceptance
will continue deployment to eks-cluster-2.

1.	Navigate to your application pipeline and select "Configure" 	

![](/images/spinnaker/eks_modify_pipeline.png)
 
2.	Click on “Add stage” and choose “Deploy Manifest” as Type, and select “eks-cluster-2” as account for manifest deployment in Basic Settings.
![](/images/spinnaker/eks_new_pipeline_3.png)
 
3.	Paste following kubernetes manifest in “Manifest configuration” 

```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  annotations:
    strategy.spinnaker.io/max-version-history: '2'
    traffic.spinnaker.io/load-balancers: '["service lb-aws2"]'
  labels:
    app: app-aws2
  name: app-aws2-frontend
spec:
  replicas: 1
  selector:
    matchLabels:
     app: app-aws2
  template:
    metadata:
     labels:
      app: app-aws2
    spec:
       containers:
         - image: index.docker.io/mbednarz/multi-eks
           name: frontend
```

4.   Move to Infrastructure Tab to create Load Balancers

![](/images/spinnaker/eks_create_lb.png)

5.   Click “Create Load Balancer”, select “eks-cluster-2" as the account and paste service manifest 

```
apiVersion: v1
kind: Service
metadata:
  name: lb-aws2
  namespace: default
spec:
  ports:
    - port: 80
      protocol: TCP
      targetPort: 8000
  selector:
    frontedBy: lb-aws2
  type: LoadBalancer
```
3.  Click “Create”

Test the pipeline by going back to Pipeline tab and clicking "Start Manual Execution". This will trigger the deployment to eks-cluster-1 and the pipeline will wait for user to click on "Manual Judgment" 
to stop or continue execution. If user chooses to continue the pipeline will deploy the same application to eks-cluster-2 and enable external access through lb-aws2 Elastic Load Balancer.

![](/images/spinnaker/eks_execute_3_step.png)
