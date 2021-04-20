---
title: "Traffic Routing with Service Mesh"
date: 2020-04-28T10:16:11-06:00
weight: 45 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

In this section we'll introduce a service mesh using App Mesh to facilitate service-to-service internal communication.  If you want to have a single logical application that includes microservices in multiple k8s clusters, this section is for you.

For this example, we're going to use a new sample application called color picker.  It's a bit more realistic for a case where we might have two related microservices deployed on different clusters.  We have a front-end service on one cluster, and back end services on the second cluster.  We may want to have tighter network and security restrictions on the second cluster since it's not directly accessible to end users.

### Architecture

As a reminder, here's the architecture we'll deploy.

![Multiple cluster networking with mesh](/images/lb/eks-lb-multiple.png)

### Deploy

#### Install Helm

If you have not already installed Helm on the Cloud9 IDE, run:

    curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

Now run:

    helm repo add eks https://aws.github.io/eks-charts

#### Install eksctl

On Cloud9, run these commands:

    curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
    sudo mv /tmp/eksctl /usr/local/bin

#### Install App Mesh components

First, let's configure App Mesh to work with our two clusters.  Run these commands:

    kubectl config use-context cluster1
    kubectl apply -k "https://github.com/aws/eks-charts/stable/appmesh-controller/crds?ref=master"
    kubectl create ns appmesh-system
    export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
    export CLUSTER_NAME=$CLUSTER1_NAME
    export IAM_ROLE_NAME="$CLUSTER_NAME-role"
    eksctl utils associate-iam-oidc-provider \
        --region=$AWS_REGION \
        --cluster $CLUSTER_NAME \
        --approve
    export OIDC_PROVIDER=$(aws eks describe-cluster --region $AWS_REGION --name $CLUSTER_NAME --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")
    read -r -d '' TRUST_RELATIONSHIP <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringEquals": {
              "${OIDC_PROVIDER}:sub": "system:serviceaccount:appmesh-system:appmesh-controller"
            }
          }
        }
      ]
    }
    EOF
    echo "${TRUST_RELATIONSHIP}" > trust.json
    aws iam create-role --role-name $IAM_ROLE_NAME --assume-role-policy-document file://trust.json --description "grant app mesh access"
    aws iam attach-role-policy --role-name $IAM_ROLE_NAME --policy-arn=arn:aws:iam::aws:policy/AWSCloudMapFullAccess
    aws iam attach-role-policy --role-name $IAM_ROLE_NAME --policy-arn=arn:aws:iam::aws:policy/AWSAppMeshFullAccess
    kubectl create serviceaccount -n appmesh-system appmesh-controller
    kubectl annotate serviceaccount -n appmesh-system appmesh-controller \
        eks.amazonaws.com/role-arn=arn:aws:iam::$AWS_ACCOUNT_ID:role/$IAM_ROLE_NAME
    helm upgrade -i appmesh-controller eks/appmesh-controller \
        --namespace appmesh-system \
        --set region=$AWS_REGION \
        --set serviceAccount.create=false \
        --set serviceAccount.name=appmesh-controller

And on the second cluster:

    kubectl config use-context cluster2
    kubectl apply -k "https://github.com/aws/eks-charts/stable/appmesh-controller/crds?ref=master"
    kubectl create ns appmesh-system
    export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
    export CLUSTER_NAME=$CLUSTER2_NAME
    export IAM_ROLE_NAME="$CLUSTER_NAME-role"
    eksctl utils associate-iam-oidc-provider \
        --region=$AWS_REGION \
        --cluster $CLUSTER_NAME \
        --approve
    export OIDC_PROVIDER=$(aws eks describe-cluster --region $AWS_REGION --name $CLUSTER_NAME --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")
    read -r -d '' TRUST_RELATIONSHIP <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
          },
          "Action": "sts:AssumeRoleWithWebIdentity",
          "Condition": {
            "StringEquals": {
              "${OIDC_PROVIDER}:sub": "system:serviceaccount:appmesh-system:appmesh-controller"
            }
          }
        }
      ]
    }
    EOF
    echo "${TRUST_RELATIONSHIP}" > trust.json
    aws iam create-role --role-name $IAM_ROLE_NAME --assume-role-policy-document file://trust.json --description "grant app mesh access"
    aws iam attach-role-policy --role-name $IAM_ROLE_NAME --policy-arn=arn:aws:iam::aws:policy/AWSCloudMapFullAccess
    aws iam attach-role-policy --role-name $IAM_ROLE_NAME --policy-arn=arn:aws:iam::aws:policy/AWSAppMeshFullAccess
    kubectl create serviceaccount -n appmesh-system appmesh-controller
    kubectl annotate serviceaccount -n appmesh-system appmesh-controller \
        eks.amazonaws.com/role-arn=arn:aws:iam::$AWS_ACCOUNT_ID:role/$IAM_ROLE_NAME
    helm upgrade -i appmesh-controller eks/appmesh-controller \
        --namespace appmesh-system \
        --set region=$AWS_REGION \
        --set serviceAccount.create=false \
        --set serviceAccount.name=appmesh-controller

#### Create Cloud Map namespace

When the mesh spans multiple clusters, we use Cloud Map for service discovery.  Let's create a namespace now.  Run this from your own workstation:

    export CLOUDMAP_NAMESPACE=svc2.svc.local
    export VPC_ID=<VPC containing the k8s clusters>
    aws servicediscovery create-private-dns-namespace \
            --name "${CLOUDMAP_NAMESPACE}" \
            --vpc "${VPC_ID}" 

#### Deploy app images into ECR

On your laptop, run these commands:

    export ECR_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    export PROJECT_NAME=k8multi
    export ECR_IMAGE_PREFIX="${ECR_URL}/${PROJECT_NAME}"
    aws ecr get-login-password --region ${AWS_REGION} | \
            docker login --username AWS --password-stdin ${ECR_URL}
    aws ecr create-repository --repository-name $PROJECT_NAME/colorapp
    aws ecr create-repository --repository-name $PROJECT_NAME/feapp
    git clone https://github.com/aws/aws-app-mesh-examples
    cd aws-app-mesh-examples/walkthroughs/howto-k8s-cross-cluster
    docker build -t ${ECR_IMAGE_PREFIX}/colorapp ./colorapp
    docker push ${ECR_IMAGE_PREFIX}/colorapp
    docker build -t ${ECR_IMAGE_PREFIX}/feapp ./feapp
    docker push ${ECR_IMAGE_PREFIX}/feapp

#### Deploy back-end app on second cluster

Download the k8s [template](/files/lb/colorapp.yaml) and upload it to the Cloud9 IDE.  Open this file and replace the string `ECR_IMAGE_PREFIX` with the value of that environment variable.

On your second cluster:

    cd ~/environment
    kubectl config use-context cluster2
    kubectl apply -f colorapp.yaml

Note this ARN for the next section:

    kubectl get virtualservice colorapp -n k8multi | sed -n 2p | awk -F ' ' '{print $2}'

#### Deploy front-end app on first cluster

Deploy the k8s [template](/files/lb/feapp.yaml) and upload it to the Cloud9 IDE.  Open this file and replace these strings:

* `colorapp-service-ARN` -> the ARN you noted in the last section
* `ECR_IMAGE_PREFIX` -> the value of that environment variable 

On your first cluster:
    
    kubectl config use-context cluster1
    kubectl apply -f feapp.yaml

#### Open security group

Finally, we need to allow communication on port 8080 from the first cluster to the second cluster.

* Note the security group used for the nodes in the first cluster
* Edit the security group used for the nodes in the second cluster.  Open port 8080 to the first cluster's security group.

### Test

Let's make sure that the front-end and back-end services can communicate.  On the first cluster, run:

    kubectl get svc -n k8multi front

Note the endpoint for the load balancer.  Now curl that endpoint using the `/color` path:

    curl <endpoint>:8080/color

You should see the answer flip evenly between `red` and `blue`, as we set the virtual router to send traffic to both back ends with equal weight.
