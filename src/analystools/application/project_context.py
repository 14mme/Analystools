from dataclasses import dataclass
from pathlib import Path

from analystools.config.loader import load_config
from analystools.config.schema import ProjectConfig


PROJECT_CONFIG_FILE = "analystools.toml"


@dataclass(frozen=True)
class ProjectContext:
    root: Path
    config: ProjectConfig

    @property
    def config_file(self) -> Path:
        return self.root / PROJECT_CONFIG_FILE

    @property
    def data_directory(self) -> Path:
        return self.root / "data"

    @property
    def raw_directory(self) -> Path:
        return self.data_directory / "raw"

    @property
    def curated_directory(self) -> Path:
        return self.data_directory / "curated"

    @property
    def analyses_directory(self) -> Path:
        return self.root / "analyses"

    @property
    def metrics_directory(self) -> Path:
        return self.root / "metrics"

    @property
    def reports_directory(self) -> Path:
        return self.root / "reports"

    @property
    def charts_directory(self) -> Path:
        return self.root / "charts"

    @property
    def outputs_directory(self) -> Path:
        return self.root / self.config.output_directory

    @property
    def internal_directory(self) -> Path:
        return self.root / ".analystools"

    @property
    def warehouse_path(self) -> Path:
        return self.root / self.config.warehouse

    @property
    def metadata_path(self) -> Path:
        return self.root / self.config.metadata

    def dataset_path(self, name: str) -> Path:
        return self.curated_directory / f"{name}.parquet"

    def metric_path(self, name: str) -> Path:
        return self.metrics_directory / f"{name}.toml"

    def analysis_path(self, name: str) -> Path:
        return self.analyses_directory / f"{name}.yaml"

def discover_project(
    start: Path | None = None,
) -> ProjectContext:
    current = (
        start or Path.cwd()
    ).resolve()

    for directory in (
        current,
        *current.parents,
    ):
        config_file = directory / PROJECT_CONFIG_FILE

        if config_file.is_file():
            config = load_config(config_file)

            return ProjectContext(
                root=directory,
                config=config,
            )

    raise RuntimeError(
        "Could not find an Analystools project. "
        f"Looked from: {current} "
        "towards filesystem root. "
        "Run 'analystools project init <name>' "
        "to create a project."
    )