from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EvidenceValue(BaseModel):
    """
    One observed value produced by an analysis.
    """

    dimensions: dict[str, Any] = Field(
        default_factory=dict
    )

    metrics: dict[str, Any] = Field(
        default_factory=dict
    )


class Evidence(BaseModel):
    """
    Traceable evidence produced by an analysis run.
    """

    evidence_id: str

    run_id: str

    analysis_name: str

    dataset: str

    dimensions: list[str] = Field(
        default_factory=list
    )

    metrics: list[str] = Field(
        default_factory=list
    )

    sql: str

    values: list[EvidenceValue] = Field(
        default_factory=list
    )

    created_at: datetime

    @property
    def row_count(self) -> int:
        return len(self.values)