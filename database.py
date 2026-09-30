import sqlite3
from datetime import datetime
import os

DB_FILE = "incidents.db"

def init_db():
    """Create incidents table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS incidents (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        root_cause TEXT,
        affected_services TEXT,
        severity TEXT,
        evidence TEXT,
        alert_ids TEXT,
        status TEXT DEFAULT 'open',
        created_at TEXT,
        resolved_at TEXT
    )""")
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_FILE}")

def save_incident(incident):
    """Save or update an incident in the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    services_str = ",".join(incident.get("affected_services", []))
    alerts_str = ",".join(incident.get("alert_ids", []))
    
    c.execute("""INSERT OR REPLACE INTO incidents 
                 (id, title, root_cause, affected_services, severity, evidence, alert_ids, status, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (incident["id"], incident["title"], incident.get("root_cause", ""),
         services_str, incident.get("severity", "medium"),
         incident.get("evidence", ""), alerts_str,
         incident.get("status", "open"), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_incident(incident_id):
    """Get a single incident from database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM incidents WHERE id=?", (incident_id,))
    row = c.fetchone()
    conn.close()
    return row

def mark_resolved(incident_id):
    """Mark an incident as resolved."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE incidents SET status=?, resolved_at=? WHERE id=?",
        ("resolved", datetime.now().isoformat(), incident_id))
    conn.commit()
    conn.close()
    print(f"✅ Incident {incident_id} marked as resolved")

def get_incident_history():
    """Get all incidents from database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM incidents ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows
