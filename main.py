import os
os.environ['AWS_REGION'] = 'us-east-1'

from strands import Agent
from tools import get_recent_alerts, get_related_metrics, create_incident_ticket

SYSTEM_PROMPT = """You are an autonomous incident triage agent for a cloud platform.

Your job:
1. Call get_recent_alerts to see current alerts.
2. Group alerts that likely share a root cause based on timing (within minutes of each other) and service dependencies.
3. For each suspected root cause group, call get_related_metrics to confirm with concrete numbers.
4. Ignore alerts that are isolated, self-resolved, or unrelated.
5. For each real incident, call create_incident_ticket with a clear root_cause explanation citing metric evidence, severity level, and affected services.

Be precise and evidence-based in root_cause -- explain WHY you believe this is the cause.
"""

agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    tools=[get_recent_alerts, get_related_metrics, create_incident_ticket]
)

response = agent("Check for incidents and triage them.")
print(response)
