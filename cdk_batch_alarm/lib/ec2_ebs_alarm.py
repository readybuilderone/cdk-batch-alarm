from signal import alarm
from constructs import Construct
from aws_cdk import (
    Duration,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
)


class EC2EBSReadBytesAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic = None, cloudwatchOKAlarmTopic: sns.ITopic = None, cloudwatchInsDataAlarmTopic: sns.ITopic = None, threshold=999999999, period=300, evaluationPeriods=1, statistic='sum', operator = cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, dtm = cloudwatch.TreatMissingData.MISSING, **kwargs):

        super().__init__(scope, id, **kwargs)
        
        metiric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='VolumeReadBytes',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        alarm = cloudwatch.Alarm(self, 'cpualarm'+instanceID,
            alarm_name= instanceName+'-ebs-readbytes-'+'Alarm',
            threshold=threshold * 1024 * period,
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

class EC2EBSWriteBytesAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic = None, cloudwatchOKAlarmTopic: sns.ITopic = None, cloudwatchInsDataAlarmTopic: sns.ITopic = None, threshold=999999999, period=300, evaluationPeriods=1, statistic='sum', operator = cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, dtm = cloudwatch.TreatMissingData.MISSING, **kwargs):

        super().__init__(scope, id, **kwargs)
        
        metiric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='VolumeWriteBytes',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        alarm = cloudwatch.Alarm(self, 'cpualarm'+instanceID,
            alarm_name= instanceName+'-ebs-writebytes-'+'Alarm',
            threshold=threshold * 1024 * period,
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

class EC2EBSReadOPSAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic = None, cloudwatchOKAlarmTopic: sns.ITopic = None, cloudwatchInsDataAlarmTopic: sns.ITopic = None, threshold=999999999, period=300, evaluationPeriods=1, statistic='sum', operator = cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, dtm = cloudwatch.TreatMissingData.MISSING, **kwargs):

        super().__init__(scope, id, **kwargs)
        
        metiric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='VolumeReadOps',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        alarm = cloudwatch.Alarm(self, 'cpualarm'+instanceID,
            alarm_name= instanceName+'-ebs-readops-'+'Alarm',
            threshold=threshold * period,
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

class EC2EBSWriteOPSAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic = None, cloudwatchOKAlarmTopic: sns.ITopic = None, cloudwatchInsDataAlarmTopic: sns.ITopic = None, threshold=999999999, period=300, evaluationPeriods=1, statistic='sum', operator = cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, dtm = cloudwatch.TreatMissingData.MISSING, **kwargs):

        super().__init__(scope, id, **kwargs)
        
        metiric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='VolumeWriteOps',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        alarm = cloudwatch.Alarm(self, 'cpualarm'+instanceID,
            alarm_name= instanceName+'-ebs-writeops-'+'Alarm',
            threshold=threshold * period,
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

class EC2EBSQueueLenAlarm(Construct):

    def __init__(self, scope: Construct, id: str,instanceID: str, instanceName:str, cloudwatchAlarmTopic:sns.ITopic = None, cloudwatchOKAlarmTopic: sns.ITopic = None, cloudwatchInsDataAlarmTopic: sns.ITopic = None, threshold=999999999, period=300, evaluationPeriods=1, statistic='avg', operator = cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD, dtm = cloudwatch.TreatMissingData.MISSING, **kwargs):

        super().__init__(scope, id, **kwargs)
        
        metiric = cloudwatch.Metric(
            namespace='AWS/EC2',
            metric_name='VolumeQueueLength',
            dimensions_map={
                'InstanceId': instanceID
            }
        )

        alarm = cloudwatch.Alarm(self, 'cpualarm'+instanceID,
            alarm_name= instanceName+'-network-queuelen-'+'Alarm',
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