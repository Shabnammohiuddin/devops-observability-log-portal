from datetime import datetime, timezone
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="DevOps Observability & Log Analytics Portal")


class LogEvent(BaseModel):
    service: str
    level: str
    message: str
    latency_ms: float


@app.post("/api/v1/logs/ingest")
def ingest_log(event: LogEvent):
    alert_triggered = event.level.upper() in {"ERROR", "CRITICAL"} or event.latency_ms > 500
    return {
        "status": "INGESTED",
        "service": event.service,
        "alertTriggered": alert_triggered,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
