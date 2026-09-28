from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class InsightEvidence(BaseModel):
    evidence_id: str

    dimensions: dict[str, Any] = Field(
        default_factory=dict
    )

    metrics: dict[str, Any] = Field(
        default_factory=dict
    )


class Insight(BaseModel):
    insight_id: str

    evidence_id: str

    analysis_name: str

    type: str

    title: str

    description: str

    importance: str = "info"

    evidence: list[InsightEvidence] = Field(
        default_factory=list
    )

    created_at: datetime