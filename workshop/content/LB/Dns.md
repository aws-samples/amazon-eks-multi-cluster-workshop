---
title: "Traffic Routing with DNS"
date: 2020-04-28T10:16:11-06:00
weight: 25 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

In this section we'll use Route 53 to set up DNS-based routing between the same microservice in two k8s clusters.  If you are concerned with using two k8s clusters for high availability, disaster recovery, or reducing latency, this section is for you.

### Architecture

As a reminder, here's the architecture we'll deploy.

![Multiple cluster networking with DNS](/images/lb/eks-lb-multiple-public-dns.png)

For the sake of simplicity, we'll use a Route 53 private hosted zone, which means that our DNS routing will only work inside our VPC.

### Deploy

#### Add external endpoints

First, let's expose our DJ service through a load balancer so we have external endpoints.  For cluster 1 and cluster 2, run:

    kubectl edit svc dj -n prod

Change the service `type` from `ClusterIP` to `LoadBalancer`.  Grab the new load balancer endpoint from the `EXTERNAL-IP` output of:

    kubectl get svc -n prod

Check the output from the DJ service:

    curl <endpoint>:9080

You should see `DJ Reporting for duty!` from each cluster.

#### DNS zone

Now let's set up a Route 53 private hosted zone in our VPC.  Download this [template](/files/lb/dns.yaml) and deploy it in CloudFormation, using these inputs:

* Stack name: Choose a name for the stack
* Elb1 and Elb2: Grab the `DNS Name` from the [ELB console](https://us-east-2.console.aws.amazon.com/ec2/v2/home?#LoadBalancers:sort=loadBalancerName) for each load balancer used by your clusters for the `prod/dj` service.
* zone1 and zone2: Grab the `Hosted zone` from the [ELB console](https://us-east-2.console.aws.amazon.com/ec2/v2/home?#LoadBalancers:sort=loadBalancerName) for each load balancer used by your clusters.
* VpcId: Choose the VPC containing your clusters.
* VpcRegion: Set this to the region your clusters are deployed in.

For today we'll use a percentage-based weighted routing policy, which works well for shifting traffic between environments.  For HA/DR scenarios you might choose a weighted routing policy or a failover policy, while for reducing latency you'd probably choose a latency-based policy.


### Test

In Cloud9, use the context for the first cluster and make sure we can use the new DNS zone.

    kubectl config use-context cluster1
    export DJ_POD_NAME=$(kubectl get pods -n prod -l app=dj -o jsonpath='{.items[].metadata.name}')
    kubectl exec -n prod -it ${DJ_POD_NAME} bash
    curl svc1.svc.local:9080
