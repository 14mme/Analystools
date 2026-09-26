from pydantic import BaseModel, Field


class ProjectSettings(BaseModel):
    name: str = Field(min_length=1)
    version: str = "0.1.0"

class StorageSettings(BaseModel):
    warehouse: str = ".analystools/warehouse.duckdb"
    metadata: str = ".analystools/metadata.db"

class OutputSettings(BaseModel):
    directory: str = "outputs"

class ProjectConfig(BaseModel):
    project: ProjectSettings
    storage: StorageSettings = StorageSettings()
    output: OutputSettings = OutputSettings()

    @property
    def name(self) -> str:
        return self.project.name

    @property
    def version(self) -> str:
        return self.project.version

    @property
    def warehouse(self) -> str:
        return self.storage.warehouse

    @property
    def metadata(self) -> str:
        return self.storage.metadata

    @property
    def output_directory(self) -> str:
        return self.output.directory