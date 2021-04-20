# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
# SPDX-License-Identifier: MIT-0

#!/bin/bash

# Cluster 1 Name & Masters Role
export CLUSTER1_NAME=$(aws cloudformation describe-stack-resources --stack-name EksMulti-eks-c1  --query "StackResources[4].PhysicalResourceId" --output text)
export CLUSTER1_ROLE_NAME=$(aws cloudformation describe-stack-resources --stack-name EksMulti-eks-c1  --query "StackResources[6].PhysicalResourceId" --output text)
export CLUSTER1_ROLE_ARN=$(aws iam get-role --role-name ${CLUSTER1_ROLE_NAME} --query 'Role.Arn' --output text)

aws eks update-kubeconfig --alias cluster1 --name $CLUSTER1_NAME --role-arn $CLUSTER1_ROLE_ARN 

# Cluster 2 Name & Masters Role
export CLUSTER2_NAME=$(aws cloudformation describe-stack-resources --stack-name EksMulti-eks-c2  --query "StackResources[4].PhysicalResourceId" --output text)
export CLUSTER2_ROLE_NAME=$(aws cloudformation describe-stack-resources --stack-name EksMulti-eks-c2  --query "StackResources[6].PhysicalResourceId" --output text)
export CLUSTER2_ROLE_ARN=$(aws iam get-role --role-name ${CLUSTER2_ROLE_NAME} --query 'Role.Arn' --output text)

aws eks update-kubeconfig --alias cluster2 --name $CLUSTER2_NAME --role-arn $CLUSTER2_ROLE_ARN 

