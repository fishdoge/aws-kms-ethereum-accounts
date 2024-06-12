#!/usr/bin/env python3

#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0

from aws_cdk import App

from aws_kms_lambda_ethereum.aws_kms_lambda_ethereum_stack import (
    AwsKmsLambdaEthereumStack,
)

KMS_KEY_ID = "f124e66e-719c-45b6-9384-06eff93d109f"

app = App()
AwsKmsLambdaEthereumStack(app, "aws-kms-lambda-ethereum", KMS_KEY_ID, "sepolia")

app.synth()
