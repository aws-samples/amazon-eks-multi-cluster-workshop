---
title: "Cleanup"
date: 2020-04-28T10:16:11-06:00
weight: 15 
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

If you used an account provided by Event Engine, you do not need to do any cleanup.  The account terminates when the event is over.

If you used your own account, please remove the Kubernetes services before terminating the clusters.  Also remove any CloudFormation stacks you created.

Use following comand to cleanup EKS clusters and dedicated VPC:

```bash
cd ~/environment/eks-multi/
cdk destroy Eks* --require-approval never

```

After cleanup is sucessful you can also delete your Cloud9 environment using AWS console.
