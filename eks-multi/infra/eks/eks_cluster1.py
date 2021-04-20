# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
# SPDX-License-Identifier: MIT-0

from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_eks as eks
import aws_cdk.aws_iam as iam
import os

c9_ip = os.environ["C9_HOSTNAME"] + '/32'

class CdkEksC1Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create SecurityGroup for the Control Plane ENIs
        eks_security_group = ec2.SecurityGroup(
            self, "EKSSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True
        )
        
        eks_security_group.add_ingress_rule(
            ec2.Peer.ipv4('10.0.0.0/16'),
            ec2.Port.all_traffic()
        )  
        eks_security_group.add_ingress_rule(
            ec2.Peer.ipv4(c9_ip),
            ec2.Port.all_traffic()
        )  

        eks_role = iam.Role(self, "EKS_Node_Role1", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchAgentServerPolicy"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKSWorkerNodePolicy"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSAppMeshFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloudMapFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEKS_CNI_Policy")]
        )
        
        self.c1_cluster = eks.Cluster(self, "EKSCluster1",
            version=eks.KubernetesVersion.V1_18,
            default_capacity=0,
            endpoint_access=eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            vpc=vpc,
            security_group=eks_security_group

        )

        self.c1_ng = self.c1_cluster.add_nodegroup_capacity("cluster1-node-group",
            instance_types=[ec2.InstanceType("m5.large")],
            desired_size=2,
            node_role=eks_role,
            min_size=1,
            max_size=3
        )
