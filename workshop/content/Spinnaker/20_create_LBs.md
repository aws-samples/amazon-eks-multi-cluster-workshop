---
title: "Services"
date: 2020-04-28T10:16:11-06:00
weight: 20
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

In order to provide external access to our sample application we need to create load balancer for our first  Kubernetes cluster. 
AWS EKS Load Balancers
AWS EKS  cluster will automatically instantiate a load balancer in our environment based on provided manifest. 

1.	Move to Infrastructure Tab to create Load Balancers
![](/images/spinnaker/eks_create_lb.png)
2.	Click “Create Load Balancer”, select “eks-cluster-1" as the account and paste service manifest 
```
apiVersion: v1
kind: Service
metadata:
  name: lb-aws1
  namespace: default
spec:
  ports:
    - port: 80
      protocol: TCP
      targetPort: 8000
  selector:
    frontedBy: lb-aws1
  type: LoadBalancer
```
3.	Click “Create”

Test the pipeline by going back to Pipeline tab and clicking "Start Manual Execution". This will trigger the deployment to eks-cluster-1 and the pipeline will wait for user to click on "Manual Judgment" 
to stop of continue execution.
![](/images/spinnaker/eks_execute_2_step.png) 
