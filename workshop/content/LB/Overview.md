---
title: "Overview"
date: 2020-04-28T10:16:11-06:00
weight: 15 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

As a quick recap, let's review how you handle both internal and external traffic in a single k8s cluster.  Internal traffic is traffic that goes between k8s applications, while external traffic is traffic that hits public endpoints offered by those applications.  External traffic may come from end users, or just from other applications that don't need to interact closely with each other.

### Single cluster

With a single k8s cluster, you deploy one or more applications, such as microservices.  Those microservices can communicate with one another through pod networking, possibly governed by network policies offered by the CNI.  External traffic, such as an API client, can access one of the microservices only if the microservice is exposed as a k8s service.  k8s services typically use a load balancer to handle external traffic and route it to one of the appropriate pods.

![Single cluster networking](/images/lb/eks-lb-single.png)

In some cases, you may choose to use a k8s ingress controller to provide more sophisticated load balancing features like path-based routing.

![Single cluster networking with ingress](/images/lb/eks-lb-single-ingress.png)

### Single cluster with service mesh

If you have several microservices, you'll probably start using a service mesh to handle internal traffic.  That lets you control which microservices can talk to one another without using k8s network policies.  A service mesh also offers other features like easy blue/green deployments, traffic load control, and observability.

![Single cluster networking with service mesh](/images/lb/eks-lb-single-mesh.png)

Some service meshes offer ingress gateways to help you get external traffic into the mesh.  Otherwise, you have to use a regular k8s load-balanced service as the entry point to the mesh.

![Single cluster networking with service mesh and gateway](/images/lb/eks-lb-single-mesh-gateway.png)

### Multiple clusters

Now let's say that we have multiple k8s clusters that need to work together.  Perhaps they offer regional endpoints for lower-latency access by end users, or we are distributing traffic between multiple clusters for better availability.

For internal traffic between k8s applications, a service mesh that spans multiple clusters is the best option.  That way, microservices can talk to one another using regular service discovery features of the mesh, rather than having to rely on public endoints exposed through a load balancer.

![Multiple cluster networking with mesh](/images/lb/eks-lb-multiple.png)

For external traffic, we have several options.  

* DNS.  We can use a global DNS service like Route 53 to direct traffic to the most appropriate k8s cluster, based on failover rules, latency, or some other policy.  Route 53 has flexible routing policies suitable to single-region or multiple-region deployments.

![Multiple cluster networking with DNS](/images/lb/eks-lb-multiple-public-dns.png)

* Global Accelerator.  We can use Global Accelerator to route traffic to the best k8s cluster based on latency and other policies.  Global Accelerator is similar to Route 53 in some respects, but uses static IPs rather than DNS.  Global Accelerator is most suitable for multi-region deployments.

![Multiple cluster networking with Global Accelerator](/images/lb/eks-lb-multiple-public-ga.png)

* Load balancing.  We can use a load balancer to route traffic between multiple k8s clusters.  This works well when the clusters are in a single AWS region, but would introduce unwanted coupling when the clusters are not in a single region.  In order to use this approach, we need to have an NLB in front of an ALB ingress; this [blog](https://aws.amazon.com/blogs/networking-and-content-delivery/using-static-ip-addresses-for-application-load-balancers/) describes one way to set that up.  We won't look at this option in more detail because it has significant drawbacks compared to the other approaches.

![Multiple cluster networking with LB](/images/lb/eks-lb-multiple-public-lb.png)

