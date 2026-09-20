from mock_alerts import ALERTS, METRICS
from datetime import datetime

def parse_time(ts):
    return datetime.fromisoformat(ts)

print("Testing tool logic without Bedrock...\n")

# Simulate what get_recent_alerts does
alerts = ALERTS
print(f"Fetched {len(alerts)} alerts:")
for a in alerts:
    print(f"  {a['id']} | {a['timestamp']} | {a['service']} | {a['type']} | {a['message']}")

print("\nGrouping alerts by time proximity (within 5 minutes) and service...")

# Simple correlation logic: group alerts within 5 min of each other
groups = []
used = set()
for a in alerts:
    if a["id"] in used:
        continue
    group = [a]
    used.add(a["id"])
    t1 = parse_time(a["timestamp"])
    for b in alerts:
        if b["id"] in used:
            continue
        t2 = parse_time(b["timestamp"])
        if abs((t1 - t2).total_seconds()) <= 300:
            group.append(b)
            used.add(b["id"])
    groups.append(group)

print(f"\nFound {len(groups)} incident group(s):\n")

for i, group in enumerate(groups, 1):
    services = list(set(g["service"] for g in group))
    print(f"--- Group {i} ---")
    print(f"Alerts: {[g['id'] for g in group]}")
    print(f"Services involved: {services}")

    if len(group) > 1:
        # Pull metrics for evidence
        evidence_lines = []
        for svc in services:
            m = METRICS.get(svc, {})
            evidence_lines.append(f"{svc}: {m}")
        evidence = " | ".join(evidence_lines)

        ticket = {
            "title": f"Incident affecting {', '.join(services)}",
            "root_cause": "Correlated alerts within 5 minutes across dependent services suggest a shared root cause.",
            "affected_services": services,
            "severity": "high" if any("connection_pool" in g["type"] for g in group) else "medium",
            "evidence": evidence,
        }
        print("INCIDENT TICKET CREATED:")
        for k, v in ticket.items():
            print(f"  {k}: {v}")
    else:
        print("Single isolated alert -- likely noise, skipping ticket creation.")
    print()

print("Logic test complete.")
