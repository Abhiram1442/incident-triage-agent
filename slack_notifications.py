import requests
import os
from datetime import datetime

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "YOUR_WEBHOOK_URL_HERE")

def send_slack_notification(incident):
    if not SLACK_WEBHOOK_URL or SLACK_WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE":
        return False

    emoji = "??" if incident["severity"] == "high" else "??"

    message = {
        "text": f"{emoji} {incident['title']}",
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": f"{emoji} {incident['id']}"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*Severity:* {incident['severity'].upper(^)}"}}
        ]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        return response.status_code == 200
    except:
        return False
