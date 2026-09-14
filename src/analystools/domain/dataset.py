from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class Dataset(BaseModel):
    name: str = Field(min_length=1)
    source: Path
    parquet_path: Path
    rows: int
    columns: int
    created_at: datetime
    source_hash: str