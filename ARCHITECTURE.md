# System Architecture

## Overview

## Data Flow

1. **Alert Fetching** (get_recent_alerts)
   - Retrieves mock/live alert data
   - Fields: id, timestamp, service, type, message

2. **Metric Correlation** (get_related_metrics)
   - Pulls service metrics for suspected root causes
   - Fields: cpu, memory, connections, pool_utilization, etc.

3. **Agent Reasoning**
   - Groups alerts by timing (within 5 minutes)
   - Correlates across service dependencies
   - Weighs urgency (connection pool > latency > error rate)

4. **Ticket Creation** (create_incident_ticket)
   - Outputs structured incident with:
     - Title, root cause, affected services, severity, evidence

## Example Incident

## Technology Stack
- **Agent Framework**: Strands Agents SDK
- **LLM**: Claude (via AWS Bedrock)
- **Data**: Mock JSON (alerts, metrics)
- **Language**: Python 3.13

