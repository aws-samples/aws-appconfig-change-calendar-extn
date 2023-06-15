#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import aws_cdk as cdk

from cdk_appconfig_change_calendar_extn.cdk_appconfig_change_calendar_extn_stack import (  # noqa: E501
    CdkAppconfigChangeCalendarExtnStack,
)


app = cdk.App()
CdkAppconfigChangeCalendarExtnStack(
    app,
    "CdkAppconfigChangeCalendarExtnStack",
)

app.synth()
