from pyclbr import Function
from aws_cdk import (
    Stack,
    aws_sqs as sqs,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
)
from constructs import Construct
from aws_cdk.aws_lambda import Function as fn
import boto3
import re
from .lib.ec2alarm import EC2StatusCheckFailedAlarm


class CdkBatchAlarmStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        SNSTopicARN = 'arn:aws:sns:ap-northeast-1:750521193989:CloudwatchAlarmTopic'
        EC2NameRegex = '^mock*'

        cloudwatchAlarmTopic = sns.Topic.from_topic_arn(self, 'cloudwatchAlarmTopic', SNSTopicARN)
        
        nametagInstanceDict = {}
        ec2_tags = self._getAllEC2Tags()
        self._getNametagInstanceDict(ec2_tags, nametagInstanceDict)
        # print(ec2_tags)
        # print(nametagInstanceDict)
        for name in nametagInstanceDict:
            if(re.search(EC2NameRegex, name)):
                # print(name, nametagInstanceDict[name])
                # self.createStatusCheckFailedAlarm(cloudwatchAlarmTopic, nametagInstanceDict[name], name)
                EC2StatusCheckFailedAlarm(self,'SystemCheckFailed'+nametagInstanceDict[name],nametagInstanceDict[name], name, cloudwatchAlarmTopic)

    # def createStatusCheckFailedAlarm(self, cloudwatchAlarmTopic, instanceID, instanceName):
    #     statusCFMetric = cloudwatch.Metric(
    #         namespace='AWS/EC2',
    #         metric_name='StatusCheckFailed',
    #         dimensions_map={
    #             "InstanceId": instanceID
    #         }
    #     )

    #     statusCFAlarm = cloudwatch.Alarm(self, 'alarm'+instanceID, 
    #         alarm_name= instanceName+'-SCF-'+'Alarm',
    #         threshold= 0,
    #         evaluation_periods=1,
    #         metric=statusCFMetric,
    #         comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
    #     )

    #     statusCFAlarm.add_alarm_action(
    #         cw_actions.SnsAction(
    #             cloudwatchAlarmTopic
    #         )
    #     )


    def _getNametagInstanceDict(self, ec2_tags, nametagInstanceDict):
        for item in ec2_tags:
            if(item['Key']=='Name'):
                nametagInstanceDict[item['Value']]=item['ResourceId']

    def _getAllEC2Tags(self):
        ec2 = boto3.client('ec2')
        ec2_tags_response = ec2.describe_tags(
            Filters=[
                {
                    'Name': 'resource-type',
                    'Values': [
                        'instance',
                    ],
                }
            ],
            MaxResults=1000
        )
        ec2_tags=ec2_tags_response['Tags']
        return ec2_tags
