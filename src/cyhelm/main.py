from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, Field


class Status(str, Enum):
    implemented = "implemented"
    partial = "partial"
    missing = "missing"
    not_applicable = "not_applicable"


class ControlAssessment(BaseModel):
    control_id: str = Field(min_length=2, max_length=40)
    title: str = Field(min_length=3, max_length=160)
    status: Status
    evidence: list[str] = Field(default_factory=list, max_length=30)
    business_impact: int = Field(ge=1, le=5)
    effort: int = Field(ge=1, le=5)
    owner: str | None = Field(default=None, max_length=100)
    applicability_rationale: str | None = Field(default=None, max_length=500)


class Finding(BaseModel):
    control_id: str
    priority: str
    score: float
    evidence_complete: bool
    remediation: str


def finding(item: ControlAssessment) -> Finding:
    status_weight = {"missing": 1.0, "partial": 0.6, "implemented": 0.0, "not_applicable": 0.0}
    score = round(status_weight[item.status.value] * item.business_impact * (6 - item.effort), 1)
    priority = "urgent" if score >= 16 else "high" if score >= 10 else (
        "medium" if score > 0 else "monitor"
    )
    evidence_complete = bool(item.evidence) if item.status != "not_applicable" else bool(
        item.applicability_rationale
    )
    return Finding(
        control_id=item.control_id,
        priority=priority,
        score=score,
        evidence_complete=evidence_complete,
        remediation=(
            "Define an owner, implementation plan, target date, and acceptance criteria."
            if item.status in {"missing", "partial"}
            else "Validate evidence and reassess at the agreed review frequency."
        ),
    )


app = FastAPI(title="CyHelm Compliance Gap Assessment", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/assessments/findings", response_model=list[Finding])
def create_findings(controls: list[ControlAssessment]) -> list[Finding]:
    return sorted((finding(item) for item in controls), key=lambda item: item.score, reverse=True)

