from __future__ import annotations

from .models import (
    AccessRequestEvent,
    CpuEvent,
    Decision,
    DiskFullEvent,
    Event,
    ServiceDegradationEvent,
)


def evaluate_rules(event: Event) -> Decision | None:
    if isinstance(event, CpuEvent):
        if event.duration_minutes < 10:
            return Decision(
                decision="ignore",
                confidence=0.9,
                rationale="Short CPU spike below 10 minutes.",
                handler="deterministic",
            )
        if event.autoscaling_available:
            return Decision(
                decision="scale_up",
                confidence=0.85,
                rationale="Autoscaling available for sustained CPU spike.",
                handler="deterministic",
            )

    if isinstance(event, AccessRequestEvent):
        if event.policy_match:
            return Decision(
                decision="auto_approve",
                confidence=0.95,
                rationale="Access request matches policy.",
                handler="deterministic",
            )

    if isinstance(event, DiskFullEvent):
        if event.cleanup_script_available and event.disk_percent >= 90:
            return Decision(
                decision="run_cleanup",
                confidence=0.88,
                rationale="Disk usage critical with cleanup script available.",
                handler="deterministic",
            )

    if isinstance(event, ServiceDegradationEvent):
        if event.error_rate_percent < 2 and event.p95_latency_ms < 500:
            return Decision(
                decision="monitor",
                confidence=0.8,
                rationale="Minor degradation within tolerance thresholds.",
                handler="deterministic",
            )

    return None
