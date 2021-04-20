---
title: "Applications"
date: 2020-04-28T10:02:27-06:00
weight: 30
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

## Deploying Applications

Let's deploy sample applications onto each of our clusters.

### DJ App

Let's deploy a sample music DJ [app](https://www.eksworkshop.com/advanced/320_servicemesh_with_appmesh/deploy_dj_app/) onto the first cluster.  

* Connect to your Cloud9 environment
* Make sure you are using the context for the first cluster: `kubectl config use-context cluster1`
* `cd ~/environment`
* Clone the sample Git repository: `git clone https://github.com/aws/aws-app-mesh-examples`
* Change into the example app directory: `cd aws-app-mesh-examples/examples/apps/djapp/`
* Deploy the app: `kubectl apply -f 1_base_application/base_app.yaml`
* Verify that the app is up and running: `kubectl -n prod get all`

You can test that the application is working correctly.  First, access the pod:

    export DJ_POD_NAME=$(kubectl get pods -n prod -l app=dj -o jsonpath='{.items[].metadata.name}')
    kubectl exec -n prod -it ${DJ_POD_NAME} bash 

Now curl the two backend services:

    curl -s jazz-v1:9080 | json_pp
    curl -s metal-v1:9080 | json_pp

You can now press `Ctrl+D` to exit the pod.

### Development environment

Let's deploy another copy of the DJ app onto our second cluster, to simulate a development environment.  Follow the same instructions as above, but using the context for the second cluster:

    kubectl config use-context cluster2
