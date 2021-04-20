
---
title: "Installation"
date: 2020-04-28T10:16:11-06:00
weight: 10
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

We'll use an existing EKS cluster to deploy Spinnaker. To do so we need to start by adding and configuring Kubernetes accounts.
Let's start by creating a separate configuration context for first EKS cluster.
Please remember to change cluster name and region parameters if you used different region and cluster name during initial cluster creation.

Enable the Kubernetes provider for Spinnaker

```
hal config provider kubernetes enable

kubectl config use-context cluster1
```

We'll create Spinnaker service account next and acquire authentication token :
```
CONTEXT=$(kubectl config current-context)
kubectl apply --context $CONTEXT -f https://www.spinnaker.io/downloads/kubernetes/service-account.yml
TOKEN=$(kubectl get secret --context $CONTEXT \
   $(kubectl get serviceaccount spinnaker-service-account \
       --context $CONTEXT \
       -n spinnaker \
       -o jsonpath='{.secrets[0].name}') \
   -n spinnaker \
   -o jsonpath='{.data.token}' | base64 --decode)

```

Set the user entry in kubeconfig:

```

kubectl config set-credentials ${CONTEXT}-token-user --token $TOKEN

kubectl config set-context $CONTEXT --user ${CONTEXT}-token-user
```

Configure Spinnaker with first EKS cluster, enable artifacts to reference objects such as container images,
and choose distributed deployment type which allows Halyard to deploy Spinnaker components as microservices.
Spinnaker will use S3 to store its configuration and artifact references.
To enable S3 access we first need to edit an IAM  role assigned to EKS Worker nodes.
Please refer to https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html for more information


```
hal config provider kubernetes account add cluster1 --context $CONTEXT
hal config features edit --artifacts true
hal config deploy edit --type distributed --account-name cluster1
hal config storage s3 edit 
hal config storage edit --type s3

```

Repeat above steps to configure, and merge second cluster EKS configuration file.

```
kubectl config use-context cluster2
```

We'll create Spinnaker service account next and acquire authentication token :
```
CONTEXT=$(kubectl config current-context)
kubectl apply --context $CONTEXT -f https://www.spinnaker.io/downloads/kubernetes/service-account.yml
TOKEN=$(kubectl get secret --context $CONTEXT \
   $(kubectl get serviceaccount spinnaker-service-account \
       --context $CONTEXT \
       -n spinnaker \
       -o jsonpath='{.secrets[0].name}') \
   -n spinnaker \
   -o jsonpath='{.data.token}' | base64 --decode)

```

Set the user entry in kubeconfig:

```

kubectl config set-credentials ${CONTEXT}-token-user --token $TOKEN

kubectl config set-context $CONTEXT --user ${CONTEXT}-token-user

hal config provider kubernetes account add cluster2 --context $CONTEXT
```



Use ``hal version list`` to list latest version of Spinnaker available for deployment, and select the latest version from 1.19.x train.
For example : 

```bash
hal config version edit --version 1.19.14
```

Deploy Spinnaker to cluster1

```
kubectl config use-context cluster1
hal deploy apply
```

Installation can take up to 10-15 minutes. You can monitor progress but issuing following command:

```bash
kubectl -n spinnaker get svc,po
```

Once all services and pods are available and ready, you can expose Spinnaker services using Elastic Load Balancer. 

```
kubectl -n spinnaker expose service spin-gate --type LoadBalancer --port 80 --target-port 8084 --name spin-gate-public 

kubectl -n spinnaker expose service spin-deck --type LoadBalancer --port 80 --target-port 9000 --name spin-deck-public  

```

Use the Elastic Load Balancer endpoints to update Spinnaker configuration:

```  
export API_URL=$(kubectl -n spinnaker get svc spin-gate-public  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
export  UI_URL=$(kubectl -n spinnaker get svc spin-deck-public -o jsonpath='{.status.loadBalancer.ingress[0].hostname}') 

hal config security api edit --override-base-url http://${API_URL} 
hal config security ui edit --override-base-url http://${UI_URL}

hal deploy apply
```

It can take several minutes for Spinnaker components to restart and start using new endpoints. You can monitor progress using the following command:
```bash
kubectl -n spinnaker get svc,po
```

Once all components are up and running issue following command to get Spinnaker UI endpoint.

```bash
kubectl -n spinnaker get svc spin-deck-public -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

Navigate to the URL in a supported browser and log in.
