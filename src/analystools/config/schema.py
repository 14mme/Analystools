from pathlib import Path

from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    name: str
    version: str = "0.1.0"

    warehouse: Path = Field(default=Path(".analystools/warehouse.duckdb"))
    metadata: Path = Field(default=Path(".analystools/metadata.db"))
    output_directory: Path = Field(default=Path("outputs"))