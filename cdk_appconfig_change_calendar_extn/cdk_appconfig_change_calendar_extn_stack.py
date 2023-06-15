"""
CDK stack to deploy the CheckChangeCalendar AppConfig Extension
"""

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0


from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda
from aws_cdk import aws_lambda_python_alpha as aws_python
from aws_cdk import custom_resources as cr
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
            assumed_by=iam.ServicePrincipal("appconfig.amazonaws.com"),
        )
        function.grant_invoke(appconfig_svc_role)

        cr.AwsCustomResource(
            self,
            "extn_cr",
            install_latest_aws_sdk=False,
            policy=cr.AwsCustomResourcePolicy.from_statements(
                statements=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "appconfig:CreateExtension",
                            "appconfig:UpdateExtension",
                            "appconfig:DeleteExtension",
                        ],
                        resources=["*"],
                    ),
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=["iam:PassRole"],
                        resources=[appconfig_svc_role.role_arn],
                    ),
                ]
            ),
            on_create=cr.AwsSdkCall(
                action="createExtension",
                service="AppConfig",
                parameters={
                    "Actions": {
                        "PRE_START_DEPLOYMENT": [
                            {
                                "Uri": function.function_arn,
                                "Name": ACTION_NAME,
                                "RoleArn": appconfig_svc_role.role_arn,
                            }
                        ]
                    },
                    "Description": EXTENSION_DESCRIPTION,
                    "Name": EXTENSION_NAME,
                    "Parameters": EXTENSION_PARAMS,
                },
                physical_resource_id=cr.PhysicalResourceId.from_response("Id"),
            ),
            on_update=cr.AwsSdkCall(
                action="updateExtension",
                service="AppConfig",
                parameters={
                    "ExtensionIdentifier": cr.PhysicalResourceIdReference(),
                    "Actions": {
                        "PRE_START_DEPLOYMENT": [
                            {
                                "Uri": function.function_arn,
                                "RoleArn": appconfig_svc_role.role_arn,
                                "Name": ACTION_NAME,
                            }
                        ]
                    },
                    "Description": EXTENSION_DESCRIPTION,
                    "Parameters": EXTENSION_PARAMS,
                },
                physical_resource_id=cr.PhysicalResourceId.from_response("Id"),
            ),
            on_delete=cr.AwsSdkCall(
                action="deleteExtension",
                service="AppConfig",
                parameters={"ExtensionIdentifier": cr.PhysicalResourceIdReference()},
                ignore_error_codes_matching="ResourceNotFoundException",
            ),
        )
