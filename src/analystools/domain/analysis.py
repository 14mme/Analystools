from datetime import datetime

from pydantic import BaseModel, Field


class Analysis(BaseModel):
    name: str = Field(min_length=1)
    dataset: str
    created_at: datetime
    parameters: dict[str, object] = Field(
        default_factory=dict
    )