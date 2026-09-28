from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class EvidenceValue(BaseModel):
    dimensions: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)


class Evidence(BaseModel):
    evidence_id: str
    run_id: str
    analysis_name: str
    dataset: str
    dimensions: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    sql: str
    values: list[EvidenceValue] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def row_count(self) -> int:
        return len(self.values)