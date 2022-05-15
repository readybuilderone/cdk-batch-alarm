from signal import alarm
from constructs import Construct
from aws_cdk import (
    Duration,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
)
import sys


class EC2NetworkInAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic = None, cloudwatchOKAlarmTopic: sns.ITopic = None, cloudwatchInsDataAlarmTopic: sns.ITopic = None, threshold= sys.maxsize, period=300, evaluationPeriods=1, statistic='avg', operator = cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, dtm = cloudwatch.TreatMissingData.MISSING, **kwargs):

        super().__init__(scope, id, **kwargs)
        
        metiric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='NetworkIn',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        alarm = cloudwatch.Alarm(self, 'cpualarm'+instanceID,
            alarm_name= instanceName+'-network-in-'+'Alarm',
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

class EC2NetworkOutAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic = None, cloudwatchOKAlarmTopic: sns.ITopic = None, cloudwatchInsDataAlarmTopic: sns.ITopic = None, threshold= sys.maxsize, period=300, evaluationPeriods=1, statistic='avg', operator = cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, dtm = cloudwatch.TreatMissingData.MISSING, **kwargs):

        super().__init__(scope, id, **kwargs)
        
        metiric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='NetworkOut',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        alarm = cloudwatch.Alarm(self, 'cpualarm'+instanceID,
            alarm_name= instanceName+'-network-out-'+'Alarm',
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