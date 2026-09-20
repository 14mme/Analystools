from pathlib import Path

from analystools.config.loader import load_config
from analystools.config.schema import ProjectConfig


PROJECT_CONFIG_NAME = "analystools.toml"


class ProjectContext:
    def __init__(
        self,
        root: Path,
        config: ProjectConfig,
    ) -> None:
        self.root = root
        self.config = config

    @property
    def warehouse_path(self) -> Path:
        return self.root / self.config.warehouse

    @property
    def metadata_path(self) -> Path:
        return self.root / self.config.metadata

    @property
    def output_directory(self) -> Path:
        return self.root / self.config.output_directory

    @property
    def data_directory(self) -> Path:
        return self.root / "data"

    @property
    def raw_data_directory(self) -> Path:
        return self.data_directory / "raw"

    @property
    def curated_data_directory(self) -> Path:
        return self.data_directory / "curated"

    @property
    def metrics_directory(self) -> Path:
        return self.root / "metrics"

    @property
    def analyses_directory(self) -> Path:
        return self.root / "analyses"

    @property
    def reports_directory(self) -> Path:
        return self.root / "reports"

    @property
    def charts_directory(self) -> Path:
        return self.root / "charts"


def discover_project(
    start: Path | None = None,
) -> ProjectContext:
    current = (
        start or Path.cwd()
    ).resolve()

    if current.is_file():
        current = current.parent

    for directory in (
        current,
        *current.parents,
    ):
        config_path = directory / PROJECT_CONFIG_NAME

        if config_path.exists():
            config = load_config(config_path)

            return ProjectContext(
                root=directory,
                config=config,
            )

    raise RuntimeError(
        "Could not find 'analystools.toml'. "
        "Make sure you are inside an Analystools project "
        "or one of its subdirectories."
    )