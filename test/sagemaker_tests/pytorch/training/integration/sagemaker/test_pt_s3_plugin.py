# Copyright 2018-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import

import os

import boto3
import pytest
from sagemaker import utils
from ...integration import (DEFAULT_TIMEOUT, resnet18_path)
from ...integration.sagemaker.timeout import timeout

MULTI_GPU_INSTANCE = 'ml.p3.8xlarge'
RESOURCE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'resources')


@pytest.mark.processor("gpu")
@pytest.mark.integration("pt_s3_plugin")
@pytest.mark.model("resnet18")
@pytest.mark.skip_cpu
@pytest.mark.skip_py2_containers
def test_pt_s3_plugin_sm_gpu(sagemaker_session, framework_version, ecr_image):
    with timeout(minutes=DEFAULT_TIMEOUT):
        pytorch = PyTorch(
            entry_point="main.py",
            source_dir=resnet18_path,
            image_uri=ecr_image,
            role='SageMakerRole',
            instance_count=1,
            instance_type=MULTI_GPU_INSTANCE,
            sagemaker_session=sagemaker_session,
            framework_version=framework_version
        )
        job_name = utils.unique_name_from_base('test-pytorch-s3-plugin')
        pytorch.fit(job_name=job_name)

