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


#Ref：https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html
class EC2CPUUtilizationAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic = None, cloudwatchOKAlarmTopic: sns.ITopic = None, cloudwatchInsDataAlarmTopic: sns.ITopic = None, threshold=0.5, period=300, evaluationPeriods=1, statistic='avg', operator = cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, dtm = cloudwatch.TreatMissingData.MISSING, **kwargs):

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
                period=Duration.seconds(period),
                statistic= statistic,
            ),
            comparison_operator= operator,
            treat_missing_data=dtm
        )

        if cloudwatchAlarmTopic:
            alarm.add_alarm_action(
                cw_actions.SnsAction(cloudwatchAlarmTopic)
            )
        if cloudwatchOKAlarmTopic:
            alarm.add_ok_action(
                cw_actions.SnsAction(cloudwatchOKAlarmTopic)
            )
        if cloudwatchInsDataAlarmTopic:
            alarm.add_insufficient_data_action(
                cw_actions.SnsAction(cloudwatchInsDataAlarmTopic)
            )