#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0

from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    BundlingOptions,
    aws_lambda,
    DockerImage,
)
from constructs import Construct


class EthLambda(Construct):

    def __init__(self, scope: Construct, id: str, dir: str, env: dict):
        super().__init__(scope, id)

        commands = [
            "if [[ -f requirements.txt ]]; then pip install --target /asset-output -r requirements.txt; fi",
            "cp --parents $(find . -name '*.py') /asset-output",
        ]

        bundling_config = BundlingOptions(
            image=DockerImage("public.ecr.aws/sam/build-python3.9:latest-x86_64"),
            command=["bash", "-xe", "-c", " && ".join(commands)],
        )

        code = aws_lambda.Code.from_asset(path=dir, bundling=bundling_config)

        lf = aws_lambda.Function(
            self,
            "Function",
            handler="lambda_function.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            environment=env,
            timeout=Duration.minutes(2),
            code=code,
            memory_size=256,
        )

        self.lf = lf


class AwsKmsLambdaEthereumStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        kms_key_id: str,
        eth_network: str = "sepolia",
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        EthLambda(
            self,
            "KmsClientEIP1559",
            dir="aws_kms_lambda_ethereum/_lambda/functions/eth_client_eip1559",
            env={
                "LOG_LEVEL": "DEBUG",
                "KMS_KEY_ID": kms_key_id,
                "ETH_NETWORK": eth_network,
            },
        )

        CfnOutput(
            self,
            "KeyID",
            value=kms_key_id,
            description="KeyID of the KMS-CMK instance used as the Ethereum identity instance",
        )
