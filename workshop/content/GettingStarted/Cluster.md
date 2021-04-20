---
title: "Cluster Creation"
date: 2020-04-28T10:02:27-06:00
weight: 20
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

## Creating EKS clusters

This first step is focused on deploying the prerequisites for the EKS multi-cluster labs. For the purpose of this lab we will use the following AWS services and software components:
* [Cloud9 IDE](https://aws.amazon.com/cloud9/)
* [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html) (Cloud Development Kit)
  
### Set up a Cloud9 IDE

1. In the AWS console, go to the [Cloud9 service](https://console.aws.amazon.com/cloud9/home/product) and select `Create environment`.  Call your new IDE `MultiEKSIDE` and click `Next Step`.  
On the next screen, select "Other instance type" and choose `m5.xlarge` instance type. Click `Next step` again.  
On the final page, click `Create environment`.  Make sure that you leave the VPC settings at the default values.

Once the environment builds, you'll automatically redirect to the IDE.  Take a minute to explore the interface, and note that you can change 
the color scheme if you like (AWS Cloud9 menu -> Preferences -> Themes).

Next, let's update the Cloud9 environment to let you run the labs from the environment.


* Create a role for your Cloud9 environment by clicking on the following [link](https://console.aws.amazon.com/iam/home#/roles$new?step=review&commonUseCase=EC2%2BEC2&selectedUseCase=EC2&policies=arn:aws:iam::aws:policy%2FAdministratorAccess)
* Confirm that AWS service and EC2 are selected, then click Next to view permissions.
* Confirm that AdministratorAccess is checked, then click Next: Tags to assign tags.
* Leave the defaults, and click Next: Review to review.
* Enter `Cloud9-Admin-Role` for the Name, and click Create role. 

* Once this new profile is created, go to EC2 and find the Cloud9 instance, and assign the instance profile to this instance.
* Go to Cloud9 Preferences and under AWS Credentials disable `AWS managed temporary credentials`.  


1. In your Cloud 9 environment, clone the Git repo:
```
git clone <GITHUB LINK TBD>
cd eks-multi
```

2. Upgrade AWS CLI according to guidance in [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html).

```bash
sudo pip install --upgrade awscli && hash -r
```

3.  Install jq, envsubst (from GNU gettext utilities) and bash-completion

```bash
sudo yum -y install jq gettext bash-completion moreutils
```

4.  Install the required Kubernetes tools for interacting with the EKS cluster.

```bash
sudo curl --silent --location -o /usr/local/bin/kubectl \
   https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.11/2020-09-18/bin/linux/amd64/kubectl

sudo chmod +x /usr/local/bin/kubectl

kubectl completion bash >>  ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion
```

5. Set account and region environmental variables

```bash
export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
echo "export ACCOUNT_ID=${ACCOUNT_ID}" | tee -a ~/.bash_profile
echo "export AWS_REGION=${AWS_REGION}" | tee -a ~/.bash_profile
aws configure set default.region ${AWS_REGION}
aws configure set default.account ${ACCOUNT_ID}
aws configure get default.region
aws configure get default.account
```

6. Prepare AWS CDK 

```bash 
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade aws-cdk.core
pip install -r requirements.txt
cdk bootstrap aws://$ACCOUNT_ID/$AWS_REGION 
cdk synth 
cdk ls 
```

7. Deploy EKS clusters 

```bash
cdk deploy EksMulti-eks-c1 EksMulti-eks-c2
```

8. Setup Kubernetes configuration files and environment variables.

```bash
source ~/environment/eks-multi/scripts/update-kube-config.sh 
```

9. Check that the contexts for all the clusters are set up:

```bash
kubectl config get-contexts
```

Notice that `cluster3` is now the current context, so we're set up to issue commands against the third cluster.  Run these commands to verify that you can access the new EKS cluster.

    kubectl version
    kubectl get nodes

### Switching cluster context

Going forward, you can run this command to use the first cluster.

    kubectl config use-context cluster1

Run this command to use the second cluster.

    kubectl config use-context cluster2
