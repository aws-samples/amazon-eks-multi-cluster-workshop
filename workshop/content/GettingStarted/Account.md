---
title: "Prerequisites"
date: 2020-04-28T10:02:27-06:00
weight: 10
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

## Prerequisites

To run this workshop, you need an AWS account, and a user identity with access to the following services:

* EKS
* EC2
* App Mesh
* CloudWatch

You can use your own account, or an account provided through Event Engine as part of an AWS organized workshop.  Using an account provided by Event Engine is the easier path, as you will have full access to all AWS services, and the account will terminate automatically when the event is over.

You should also have familiarity with using the AWS CLI, including configuring the CLI for a specific account and region profile.  If not, please follow the [CLI setup instructions](https://github.com/aws/aws-cli).  Make sure you have a default profile set up; you may need to run `aws configure` if you have never set up the CLI before.

### Account setup 

#### Using an account provided through Event Engine

If you are running this workshop as part of an Event Engine lab, please log into the console using [this link](https://dashboard.eventengine.run/) and enter the hash provided to you as part of the workshop.

#### Using your own AWS account

If you are using your own AWS account, be sure you have access to create and manage resources in EKS, EC2, App Mesh, and CloudWatch.

*After completing the workshop, remember to complete the [cleanup](/next) section to remove any unnecessary AWS resources.*

#### Note your account and region

After you have your account identified, pick an AWS region to work in, such as `us-west-2`.  We'll refer to this as `REGION` going forward.  This workshop should work in `us-east-1`, `us-east-2`, or `us-west-2`.  You can likely use it in other regions but may have to make some minor adjustments to the CloudFormation templates.

Also note your AWS account number.  You find this in the console or by running `aws sts get-caller-identity` on the CLI.  We'll refer to this as `ACCOUNT` going forward.


