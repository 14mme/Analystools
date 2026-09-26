from pydantic import BaseModel, Field


class OrderBy(BaseModel):
    field: str = Field(min_length=1)
    direction: str = "ASC"

    def normalized_direction(self) -> str:
        direction = self.direction.upper()

        if direction not in {"ASC", "DESC"}:
            raise ValueError(
                f"Invalid order direction: {self.direction}"
                "use ASC or DESC"
                )

        return direction

class AnalysisDefinition(BaseModel):
    name: str = Field(min_length=1)
    dataset: str = Field(min_length=1)

    dimensions: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)

    order_by: list[OrderBy] = Field(default_factory=list)

class AnalysisFile(BaseModel):
    analysis: AnalysisDefinition

class AnalysisResult(BaseModel):
    analysis_id: str
    analysis_name: str
    dataset: str

    dimensions: list[str]
    metrics: list[str]

    columns: list[str]
    rows: list[tuple]

    sql: str
    execution_time_ms: float