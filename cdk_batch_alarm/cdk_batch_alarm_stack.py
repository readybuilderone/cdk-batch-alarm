from pyclbr import Function
from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
)
from constructs import Construct
from aws_cdk.aws_lambda import Function as fn
import boto3


class CdkBatchAlarmStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        queue = sqs.Queue(
            self, "CdkBatchAlarmQueue",
            visibility_timeout=Duration.seconds(300),
        )

        ec2_tags = self.getAllEC2Tags()
        print(ec2_tags)

        nametagInstanceDict = {}
        self.getNametagInstanceDict(ec2_tags, nametagInstanceDict)
        print(nametagInstanceDict)

        for name in nametagInstanceDict:
            print(name, nametagInstanceDict[name])
        
        statusCFMetric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='StatusCheckFailed',
            dimensions_map={
                "InstanceId": 'i-0b73e158a02d010f8'
            }
        )

        cloudwatch.Alarm(self, 'alarm', 
            threshold= 0,
            evaluation_periods=2,
            metric=statusCFMetric,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        )


    def getNametagInstanceDict(self, ec2_tags, nametagInstanceDict):
        for item in ec2_tags:
            if(item['Key']=='Name'):
                nametagInstanceDict[item['Value']]=item['ResourceId']

    def getAllEC2Tags(self):
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
