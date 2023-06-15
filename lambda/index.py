"""
AWS AppConfig Extension

Use for PRE_START_DEPLOYMENT hook; verifies that the specified SSM Change
Calendars are open and blocks deployment if not.
"""

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3

ssm = boto3.client("ssm")


def lambda_handler(event, context):
    print(event)
    calendar_list = list(
        map(str.strip, event["Parameters"].get("calendars", "").split(","))
    )
    if len(calendar_list) == 0:
        raise ValueError("missing calendar name(s)")
    calendar_state = ssm.get_calendar_state(CalendarNames=calendar_list)
    if calendar_state["State"] == "CLOSED":
        return {
            "statusCode": 200,
            "Error": "Blocked",
            "Message": "Calendar is currently closed; try again after "
            + calendar_state["NextTransitionTime"],
        }
    return {
        "statusCode": 200,
    }
