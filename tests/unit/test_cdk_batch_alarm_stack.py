import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_batch_alarm.cdk_batch_alarm_stack import CdkBatchAlarmStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_batch_alarm/cdk_batch_alarm_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkBatchAlarmStack(app, "cdk-batch-alarm")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
