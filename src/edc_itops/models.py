from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class EventType(StrEnum):
    cpu_threshold_breach = "CPU_THRESHOLD_BREACH"
    access_request = "ACCESS_REQUEST"
    disk_full = "DISK_FULL"
    service_degradation = "SERVICE_DEGRADATION"


class BaseEvent(BaseModel):
    event_type: EventType
    service: str = Field(..., description="Service or system name")
    host: str = Field(..., description="Source host or asset ID")
    timestamp: str = Field(..., description="ISO-8601 event timestamp")


class CpuEvent(BaseEvent):
    event_type: Literal[EventType.cpu_threshold_breach]
    cpu_percent: float = Field(..., ge=0, le=100)
    duration_minutes: int = Field(..., ge=1)
    autoscaling_available: bool = False


class AccessRequestEvent(BaseEvent):
    event_type: Literal[EventType.access_request]
    requester: str
    resource: str
    policy_match: bool


class DiskFullEvent(BaseEvent):
    event_type: Literal[EventType.disk_full]
    disk_percent: float = Field(..., ge=0, le=100)
    cleanup_script_available: bool


class ServiceDegradationEvent(BaseEvent):
    event_type: Literal[EventType.service_degradation]
    error_rate_percent: float = Field(..., ge=0, le=100)
    p95_latency_ms: int = Field(..., ge=0)


Event = CpuEvent | AccessRequestEvent | DiskFullEvent | ServiceDegradationEvent


class Decision(BaseModel):
    decision: str
    confidence: float = Field(..., ge=0, le=1)
    rationale: str
    handler: Literal["deterministic", "cognitive"]
