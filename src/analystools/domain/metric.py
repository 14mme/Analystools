from pydantic import BaseModel, Field


class Metric(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""
    expression: str = Field(min_length=1)
    format: str = "number"