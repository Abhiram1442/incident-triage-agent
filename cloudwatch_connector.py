import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

def get_real_cloudwatch_alarms():
    try:
        response = cloudwatch.describe_alarms(StateValue="ALARM", MaxRecords=100)
        alarms = []
        for alarm in response.get("MetricAlarms", []):
            alert = {
                "id": alarm["AlarmName"][:3].upper(),
                "timestamp": datetime.now().isoformat(),
                "service": alarm.get("Dimensions", [{}])[0].get("Value", "unknown"),
                "type": "cloudwatch_alarm",
                "message": alarm.get("AlarmDescription", alarm["AlarmName"]),
                "state": alarm["StateValue"],
            }
            alarms.append(alert)
        return alarms
    except:
        return []
