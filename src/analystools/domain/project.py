from pathlib import Path

from pydantic import BaseModel, Field


class Project(BaseModel):
    name: str = Field(min_length=1)
    version: str = "0.1.0"
    root: Path
    warehouse: Path
    metadata: Path
    output_directory: Path

    @property
    def config_file(self) -> Path:
        return self.root / "analystools.toml"