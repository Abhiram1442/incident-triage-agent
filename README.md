# Autonomous Incident Triage Agent

An autonomous AI agent that monitors system alerts, correlates related signals, identifies root causes, and automatically creates structured incident tickets.

**Built with:** AWS Bedrock, Claude via Bedrock, Strands Agents SDK

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install strands-agents boto3
```

## Run
```bash
# Local logic test (no API)
python test_logic.py

# Full agent with Bedrock (requires AWS credentials)
python main.py
```

## How it works
1. Fetches recent alerts from monitoring
2. Groups alerts by timing & service dependencies
3. Pulls metrics to confirm hypotheses
4. Creates incident tickets with evidence-based root cause analysis

## Files
- `mock_alerts.py` — Sample alert & metric data
- `tools.py` — Agent tool definitions  
- `main.py` — Strands agent with Bedrock integration
- `test_logic.py` — Local logic verification (no API)

## Demo Output
The agent correctly:
- Groups A1, A2, A3 as one incident (checkout-api + checkout-db DB pool exhaustion)
- Isolates A4 as noise (unrelated auth-service event)
- Cites metric evidence: `db_pool_used: 98%`, `connections: 98/100`
- Assigns high severity due to connection pool type
