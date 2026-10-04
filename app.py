from flask import Flask, render_template, jsonify, request
from mock_alerts import get_alerts, METRICS
from database import init_db, save_incident, mark_resolved
from datetime import datetime
import json

app = Flask(__name__, template_folder='templates')

# Initialize database on startup
try:
    init_db()
except Exception as e:
    print(f"⚠️  Database init warning: {e}")

def parse_time(ts):
    return datetime.fromisoformat(ts)

def analyze_alerts():
    alerts = get_alerts()
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
    
    incidents = []
    for group in groups:
        services = list(set(g["service"] for g in group))
        
        if len(group) > 1:
            evidence_lines = []
            for svc in services:
                metrics = METRICS.get(svc, {})
                evidence_lines.append(f"{svc}: {metrics}")
            
            incident = {
                "id": f"INC-{len(incidents) + 1}",
                "title": f"Incident affecting {', '.join(services)}",
                "root_cause": "Correlated alerts within 5 minutes across dependent services suggest a shared root cause.",
                "affected_services": services,
                "severity": "high" if any("connection_pool" in g["type"] for g in group) else "medium",
                "evidence": " | ".join(evidence_lines),
                "alert_ids": [g["id"] for g in group],
                "status": "open"
            }
            incidents.append(incident)
            save_incident(incident)
        else:
            alert = group[0]
            incident = {
                "id": f"NOISE-{alert['id']}",
                "title": f"Isolated alert: {alert['message']}",
                "root_cause": "Single alert with no correlated events - likely transient.",
                "affected_services": [alert["service"]],
                "severity": "low",
                "evidence": f"Service: {alert['service']}, Metrics: {METRICS.get(alert['service'], {})}",
                "alert_ids": [alert["id"]],
                "status": "resolved"
            }
            incidents.append(incident)
            save_incident(incident)
    
    return incidents

@app.route('/')
def home():
    incidents = analyze_alerts()
    stats = {
        "total": len(incidents),
        "open": len([i for i in incidents if i["status"] == "open"]),
        "resolved": len([i for i in incidents if i["status"] == "resolved"]),
    }
    return render_template('index.html', incidents=incidents, stats=stats)

@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    return jsonify(analyze_alerts())

@app.route('/api/resolve/<incident_id>', methods=['POST'])
def resolve_incident(incident_id):
    """Mark an incident as resolved."""
    try:
        mark_resolved(incident_id)
        return jsonify({"status": "success", "message": f"Incident {incident_id} resolved"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/export/json', methods=['GET'])
def export_json():
    """Export incidents as JSON."""
    incidents = analyze_alerts()
    return jsonify({
        "exported_at": datetime.now().isoformat(),
        "count": len(incidents),
        "incidents": incidents
    })

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export incidents as CSV."""
    import csv
    from io import StringIO
    
    incidents = analyze_alerts()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Title', 'Severity', 'Status', 'Services', 'Root Cause', 'Alerts'])
    
    for inc in incidents:
        writer.writerow([
            inc['id'],
            inc['title'],
            inc['severity'],
            inc['status'],
            ','.join(inc['affected_services']),
            inc['root_cause'][:100],
            ','.join(inc['alert_ids'])
        ])
    
    response = app.response_class(
        response=output.getvalue(),
        status=200,
        mimetype="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=incidents.csv"
    return response

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Incident Triage Web App Starting")
    print("=" * 50)
    print("📊 Dashboard: http://localhost:5000")
    print("📥 Export JSON: http://localhost:5000/api/export/json")
    print("📥 Export CSV: http://localhost:5000/api/export/csv")
    print("=" * 50)
    app.run(debug=True, port=5000)