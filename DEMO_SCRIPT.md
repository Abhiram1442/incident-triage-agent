# Demo Script (5 minutes)

## [00:00-00:30] Problem Statement
"In cloud platforms, when multiple systems fail at once, engineers waste time manually connecting the dots between alerts. A DB connection pool maxes out → API errors spike → latency jumps. All three alerts come in, but nobody knows they're the same root cause.

This agent solves that by automatically correlating related alerts, pulling evidence from metrics, and creating a single actionable incident ticket."

## [00:30-01:00] Show the Data
"Here's our mock scenario: 4 alerts across two services."

Show `test_logic.py` output or the alerts in `mock_alerts.py`:
- A1: checkout-api, high error rate
- A2: checkout-db, connection pool at 98%
- A3: checkout-api, latency spike
- A4: auth-service, brief spike (noise)

## [01:00-02:30] Run the Logic
"Let me run the agent's reasoning logic locally."

Run:
```bash
python test_logic.py
```

Show output. Point out:
- Agent groups A1, A2, A3 as ONE incident
- Correctly ignores A4 (isolated, unrelated)
- Cites evidence: "db_pool_used: 98%, connections: 98/100"
- Marks severity as HIGH (connection pool is critical)

## [02:30-03:30] Show the Code
"Here's how it works under the hood."

Show snippets:
- `tools.py` — the three tools (fetch alerts, get metrics, create ticket)
- `main.py` — system prompt telling Claude how to reason about incidents

Explain:
"The agent calls these tools in sequence, reasons about what it learned, and decides if alerts are related or noise."

## [03:30-04:30] Live Demo (if quota allows)
"And here's the full agent in action with Claude via AWS Bedrock."

Run:
```bash
python main.py
```

Show the output (agent's reasoning + incident ticket created).

**If it throttles:** "The account is quota-limited, but locally we've proven the logic works perfectly."

## [04:30-05:00] Closing
"This agent scales from a single incident to monitoring enterprise-scale systems. It reduces MTTR (mean time to resolution) by automatically surfacing root causes before humans have to guess.

Built with Strands Agents SDK and AWS Bedrock, it shows how AI reasoning can automate the high-judgment work that engineers do manually every day."

---

## Key Points to Emphasize
✓ Automated correlation (not manual lookup)
✓ Evidence-based reasoning (cites metrics)
✓ Ignores noise (A4 correctly isolated)
✓ Structured output (incident tickets)
✓ Realistic scenario (DB exhaustion → cascading failures)

