# Sample AWS AppConfig Extension: Change Calendar

This sample contains an [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)
[Extension](https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html)
which verifies that specified AWS Systems Manager [Change Calendars](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-change-calendar.html)
are open before proceeding with the deployment.

The Lambda function for the extension itself is in `lambda/index.py`; the CDK
stack is here to deploy it with the correct IAM permissions, and create an
AppConfig Extension.

## Prerequisites

Please see the [AWS AppConfig
documentation](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)
for details on configuring the service.

Please see the [Systems Manager Change Calendar
documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-change-calendar.html)
for details on setting up Change Calendars.

Ensure you have an up-to-date Python install available, and [AWS CDK
v2](https://docs.aws.amazon.com/cdk/v2/guide/home.html) installed.

You will need Docker installed and running for CDK to build the Lambda function.

## Setting up

1. Clone this repo
2. In the cloned repo, create a Python virtual environment: `python -m venv .venv`
3. Activate your virtual environment: `source .venv/bin/activate`
4. Install the Python dependencies: `pip install -r requirements.txt`
5. Ensure you have suitable AWS credentials configured in your environment

## Usage

1. Have a(t least one) SSM Change Calendar
2. Deploy this CDK app: `cdk deploy`. You only need to deploy it once per AWS
   Account/Region.
3. Navigate to the AppConfig console, then choose **Extensions**
4. Choose the **ChangeCalendar** extension, then choose **Add to resource**
5. Choose the **Resource Type** to associate the Extension with, and populate
   the following fields as required
6. Under **Parameters**, for **calendars**, enter the name of your SSM Change
   Calendar. You can enter more than one by separating the names with commas
7. Choose **Create Association to Resource**

## Un-usage

1. Navigate to the AppConfig console, then choose **Extensions**
2. Choose the **ChangeCalendar** extension
3. For each entry under **Associated resources**, choose the radio button then
   choose **Remove association**, then choose **Delete**
4. Once you have removed all the Associated resources, you can `cdk destroy`
   the app

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
