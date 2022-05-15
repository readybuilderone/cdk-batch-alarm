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
from .lib.ec2_status_alarm import EC2StatusCheckFailedAlarm
from .lib.ec2_cpu_alarm import EC2CPUUtilizationAlarm


class CdkBatchAlarmStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        AlarmSNSTopicARN = 'arn:aws:sns:ap-northeast-1:750521193989:CloudwatchAlarmTopic'
        OKSNSTopicARN = 'arn:aws:sns:ap-northeast-1:750521193989:CloudwatchAlarmTopic'
        EC2NameRegex01 = '^mock*'
        EC2NameRegex02 = '^aws*'

        cloudwatchAlarmTopic = sns.Topic.from_topic_arn(self, 'cloudwatchAlarmTopic', AlarmSNSTopicARN)
        cloudwatchOKTopic = sns.Topic.from_topic_arn(self, 'cloudwatchOKTopic', OKSNSTopicARN)
        
        nametagInstanceDict = {}
        ec2_tags = self._getAllEC2Tags()
        self._getNametagInstanceDict(ec2_tags, nametagInstanceDict)
        # print(ec2_tags)
        # print(nametagInstanceDict)
        for name in nametagInstanceDict:
            if(re.search(EC2NameRegex01, name)):
                pass
                # print(name, nametagInstanceDict[name])
                EC2StatusCheckFailedAlarm(scope =self, id ='SystemCheckFailed'+nametagInstanceDict[name], instanceID=nametagInstanceDict[name], instanceName=name, cloudwatchAlarmTopic = cloudwatchAlarmTopic ,cloudwatchOKAlarmTopic= cloudwatchOKTopic)
            if(re.search(EC2NameRegex02, name)):
                print(name, nametagInstanceDict[name])
                EC2CPUUtilizationAlarm(self, id='CPUUtilization'+nametagInstanceDict[name], instanceID= nametagInstanceDict[name], instanceName= name, cloudwatchAlarmTopic= cloudwatchAlarmTopic)

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
