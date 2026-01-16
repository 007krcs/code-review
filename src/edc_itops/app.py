from __future__ import annotations

from fastapi import FastAPI

from .models import Decision, Event
from .rules import evaluate_rules

app = FastAPI(title="EDC-ITOps")

EVENT_LOG: list[Event] = []
DECISIONS: list[Decision] = []


class CognitiveResolver:
    def resolve(self, event: Event) -> Decision:
        return Decision(
            decision="needs_review",
            confidence=0.55,
            rationale="No deterministic rule matched; requires operator review.",
            handler="cognitive",
        )


resolver = CognitiveResolver()


@app.post("/events", response_model=Decision)
async def ingest_event(event: Event) -> Decision:
    EVENT_LOG.append(event)
    decision = evaluate_rules(event)
    if decision is None:
        decision = resolver.resolve(event)
    DECISIONS.append(decision)
    return decision


@app.get("/events")
async def list_events() -> list[Event]:
    return EVENT_LOG


@app.get("/decisions")
async def list_decisions() -> list[Decision]:
    return DECISIONS
