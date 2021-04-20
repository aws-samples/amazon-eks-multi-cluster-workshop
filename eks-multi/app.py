# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 
# SPDX-License-Identifier: MIT-0

#!/usr/bin/env python3

from aws_cdk import core
from infra.vpc_base.vpc import CdkVpcStack
from infra.eks.eks_cluster1 import CdkEksC1Stack
from infra.eks.eks_cluster2 import CdkEksC2Stack
from infra.eks.eks_cluster3 import CdkEksC3Stack



class EksMulti(core.App):

        def __init__(self, **kwargs): 
            super().__init__(**kwargs)

            self.stack_name = "EksMulti"
            self.base_module = CdkVpcStack(self, self.stack_name + "-base")
            self.eks_module_1 = CdkEksC1Stack(self, self.stack_name + "-eks-c1", self.base_module.vpc)
            self.eks_module_2 = CdkEksC2Stack(self, self.stack_name + "-eks-c2", self.base_module.vpc)
            self.eks_module_3 = CdkEksC3Stack(self, self.stack_name + "-eks-c3", self.base_module.vpc)

if __name__ == '__main__':
    app = EksMulti()
    app.synth()
