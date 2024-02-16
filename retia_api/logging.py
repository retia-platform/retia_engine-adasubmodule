from retia_api.models import ActivityLog
from datetime import datetime

def activity_log(severity, instance, category, messages):
    log=ActivityLog(time=datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z"), severity=severity, instance=instance, category=category, messages=messages)
    log.save()
