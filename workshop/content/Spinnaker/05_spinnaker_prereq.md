---
title: "Prerequisites"
date: 2020-04-28T10:16:11-06:00
weight: 5
---

// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
// SPDX-License-Identifier: CC-BY-SA-4.0

Connect to your Cloud9 instance and prepare your environment to install Halyard

Run below commands to install Java 11 

```
    sudo amazon-linux-extras install java-openjdk11 -y
```

Install Halyard. Please use ec2-user as the target user for Halyard installation.

```
curl -O https://raw.githubusercontent.com/spinnaker/halyard/master/install/debian/InstallHalyard.sh
sudo bash InstallHalyard.sh
```

Use 'ec2-user' when prompted for a non-root user to run Halyard.
Verify you are using Halyard version 1.40 or newer

```
hal -v
```
