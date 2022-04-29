from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
)

class EC2StatusCheckFailedAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic, threshold=1, evaluationPeriods=1, **kwargs):
        super().__init__(scope, id, **kwargs)

        statusCFMetric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='StatusCheckFailed',
            dimensions_map={
                "InstanceId": instanceID
            }
        )

        statusCFAlarm = cloudwatch.Alarm(self, 'alarm'+instanceID, 
            alarm_name= instanceName+'-SCF-'+'Alarm',
            threshold= threshold,
            evaluation_periods=evaluationPeriods,
            metric=statusCFMetric,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        )

        statusCFAlarm.add_alarm_action(
            cw_actions.SnsAction(
                cloudwatchAlarmTopic
            )
        )