from signal import alarm
from constructs import Construct
from aws_cdk import (
    Duration,
    aws_lambda as _lambda,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
)
from aws_cdk.aws_lambda import Function as fn

class EC2StatusCheckFailedAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic, threshold=1, evaluationPeriods=1, **kwargs):
        super().__init__(scope, id, **kwargs)

        statusCFMetric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='StatusCheckFailed',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        statusCFAlarm = cloudwatch.Alarm(self, 'scfalarm'+instanceID, 
            alarm_name= instanceName+'-SCF-'+'Alarm',
            threshold= threshold,
            evaluation_periods=evaluationPeriods,
            metric=statusCFMetric.with_(
                period=Duration.minutes(1),
                statistic='max'
            ),
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        )

        statusCFAlarm.add_alarm_action(
            cw_actions.SnsAction(cloudwatchAlarmTopic)
        )


#Ref：https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html
class EC2CPUUtilizationAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic, threshold=0.5, evaluationPeriods=1, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        metiric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='CPUUtilization',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        alarm = cloudwatch.Alarm(self, 'cpualarm'+instanceID,
            alarm_name= instanceName+'-cpu-'+'Alarm',
            threshold=threshold,
            evaluation_periods=evaluationPeriods,
            metric=metiric.with_(
                period=Duration.minutes(5),
                statistic='avg',
            ),
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
        )

        alarm.add_alarm_action(
            cw_actions.SnsAction(cloudwatchAlarmTopic)
        )