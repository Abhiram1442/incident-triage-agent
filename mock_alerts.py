from cloudwatch_connector import get_real_cloudwatch_alarms

def get_alerts():
    """Try real CloudWatch first, fallback to mock"""
    real_alerts = get_real_cloudwatch_alarms()
    if real_alerts:
        return real_alerts
    
    # Fallback: Return mock alerts if CloudWatch unavailable
    return [
        {"id": "A1", "timestamp": "2026-09-30T05:15:00", "service": "checkout-api", "type": "high_error_rate", "message": "5xx errors spiked to 12%"},
        {"id": "A2", "timestamp": "2026-09-30T05:14:30", "service": "checkout-db", "type": "connection_pool", "message": "DB connection pool at 98% utilization"},
        {"id": "A3", "timestamp": "2026-09-30T05:13:45", "service": "checkout-api", "type": "latency", "message": "p99 latency up 400%"},
        {"id": "A4", "timestamp": "2026-09-30T04:15:00", "service": "auth-service", "type": "high_error_rate", "message": "brief 5xx spike, self-resolved"},
    ]

METRICS = {
    "checkout-api": {"cpu": 45, "memory": 60, "active_connections": 240, "db_pool_used": "98%"},
    "checkout-db": {"cpu": 30, "connections": 98, "max_connections": 100},
    "auth-service": {"cpu": 20, "memory": 30, "error_count_last_hour": 3},
}