# Event-Driven Cognitive IT Ops (EDC-ITOps)

Production-oriented starter for an event-driven IT ops decision engine. The service resolves common events with deterministic rules and escalates to a cognitive resolver only when rules do not match.

## Architecture

```
[ Monitoring / Ticket / Alert ]
              ↓
        [ Event Gateway ]
              ↓
          [ Event Bus ]
              ↓
   [ Deterministic Ops Handlers ]
        ↓            ↓
     resolved    uncertainty
        ↓            ↓
      close   [ Cognitive Resolver ]
                        ↓
                  [ Decision + Explanation ]
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn edc_itops.app:app --reload
```

## Example event payloads

CPU threshold breach:

```json
{
  "event_type": "CPU_THRESHOLD_BREACH",
  "service": "billing-api",
  "host": "vm-23",
  "timestamp": "2026-01-01T10:21:00Z",
  "cpu_percent": 92,
  "duration_minutes": 12,
  "autoscaling_available": true
}
```

Access request:

```json
{
  "event_type": "ACCESS_REQUEST",
  "service": "identity",
  "host": "iam-01",
  "timestamp": "2026-01-01T10:21:00Z",
  "requester": "jane.doe",
  "resource": "finance-reports",
  "policy_match": true
}
```

Disk full:

```json
{
  "event_type": "DISK_FULL",
  "service": "data-warehouse",
  "host": "db-11",
  "timestamp": "2026-01-01T10:21:00Z",
  "disk_percent": 93,
  "cleanup_script_available": true
}
```

Service degradation:

```json
{
  "event_type": "SERVICE_DEGRADATION",
  "service": "payments",
  "host": "svc-02",
  "timestamp": "2026-01-01T10:21:00Z",
  "error_rate_percent": 1.4,
  "p95_latency_ms": 420
}
```
