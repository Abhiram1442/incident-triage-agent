from strands import tool
from mock_alerts import ALERTS, METRICS

@tool
def get_recent_alerts() -> list:
    """Fetch recent unresolved alerts from monitoring."""
    return ALERTS

@tool
def get_related_metrics(service: str) -> dict:
    """Get current metrics for a given service."""
    return METRICS.get(service, {})

@tool
def create_incident_ticket(title: str, root_cause: str, affected_services: list, severity: str, evidence: str) -> dict:
    """Create a structured incident ticket with the agent's analysis."""
    ticket = {
        "title": title,
        "root_cause": root_cause,
        "affected_services": affected_services,
        "severity": severity,
        "evidence": evidence,
    }
    print("INCIDENT CREATED:", ticket)
    return ticket
