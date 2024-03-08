"""
CDK stack to deploy the CheckChangeCalendar AppConfig Extension
"""

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0


from typing import cast

from aws_cdk import Stack, aws_appconfig
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda
from aws_cdk import aws_lambda_python_alpha as aws_python
from constructs import Construct

ACTION_NAME = "CheckChangeCalendar"
EXTENSION_NAME = "ChangeCalendar"
EXTENSION_DESCRIPTION = "Ensures deployments are not blocked by an SSM Change Calendar"
EXTENSION_PARAMS = {
    "calendars": {
        "Description": "Comma-separated list of SSM Change Calendar names to check against",  # noqa: E501
        "Required": True,
    }
}


class CdkAppconfigChangeCalendarExtnStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function = aws_python.PythonFunction(
            self,
            "check_fn",
            index="index.py",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="lambda_handler",
            entry="lambda",
        )
        function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["ssm:GetCalendarState"],
                resources=["*"],
            )
        )

        appconfig_svc_role = iam.Role(
            self,
            "appconfig_role",
            assumed_by=cast(
                iam.IPrincipal, iam.ServicePrincipal("appconfig.amazonaws.com")
            ),
        )
        function.grant_invoke(appconfig_svc_role)

        aws_appconfig.Extension(
            self,
            "ChangeCalExtn",
            actions=[
                aws_appconfig.Action(
                    action_points=[aws_appconfig.ActionPoint.PRE_START_DEPLOYMENT],
                    description=EXTENSION_DESCRIPTION,
                    event_destination=aws_appconfig.LambdaDestination(
                        cast(aws_lambda.IFunction, function)
                    ),
                )
            ],
            extension_name=EXTENSION_NAME,
            description=EXTENSION_DESCRIPTION,
            latest_version_number=1,
            parameters=[
                aws_appconfig.Parameter.required(
                    name="calendars",
                    description="Comma-separated list of SSM Change Calendar names to check against",
                    # TODO value is required but we don't need it
                    value=""
                ),
            ],
        )
