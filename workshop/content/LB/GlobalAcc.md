---
title: "Traffic Routing with Global Accelerator"
date: 2020-04-28T10:16:11-06:00
weight: 35 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

In this section we'll use Global Accelerator to set up routing between the same microservice in two k8s clusters.  If you are concerned with using two k8s clusters for high availability, disaster recovery, or reducing latency, this section is for you.  

Using Global Accelerator is conceptually similar to using Route 53.  However, it offers the advantage of onboarding traffic to the AWS network more quickly, which can improve performance in many cases.

### Architecture

As a reminder, here's the architecture we'll deploy.

![Multiple cluster networking with Global Accelerator](/images/lb/eks-lb-multiple-public-ga.png)

### Deploy

#### Change external endpoints to use NLB

In the previous section, we set up public service endpoints for the DJ service in each cluster.  These endpoints use a classic ELB by default.  Let's change them to use NLB, since Global Accelerator does not support the classic ELB.

On each of the two clusters, run:

    kubectl edit svc dj -n prod

Add the annotation `service.beta.kubernetes.io/aws-load-balancer-type: nlb` to the service.  Grab the new NLB endpoint from the `EXTERNAL-IP` output of:

    kubectl get svc -n prod

Check the output from the DJ service:

    curl <endpoint>:9080

You should see `DJ Reporting for duty!` from each cluster.

#### Global Accelerator

Now let's set up a Global Accelerator configuration.  Download this [template](/files/lb/gacc.yaml) and deploy it in CloudFormation, using these inputs:

* Stack name: Choose a name for the stack
* Nlb1 and Nlb2: Grab the `ARN` from the [ELB console](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#LoadBalancers:sort=loadBalancerName) for each load balancer used by your clusters.
* EndpointRegion: Set this to the region your clusters are deployed in.

### Test

From the bastion host, curl the new Global Accelerator endpoint, which you can find from the output of the CloudFormation stack:

    curl <Global Accelerator endpoint>:9080

You should get a response from one of the DJ service endpoints.  If you look at the metrics in each cluster, over time you would see the traffic distributed evenly between the clusters.
