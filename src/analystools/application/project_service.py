from pathlib import Path

from analystools.config.schema import ProjectConfig
from analystools.domain.project import Project
from analystools.infrastructure.storage.sqlite import MetadataStore


def create_project(
    root: Path,
    name: str,
) -> Project:
    root.mkdir(parents=True, exist_ok=True)

    data_dir = root / "data"
    raw_dir = data_dir / "raw"
    curated_dir = data_dir / "curated"
    analyses_dir = root / "analyses"
    metrics_dir = root / "metrics"
    reports_dir = root / "reports"
    charts_dir = root / "charts"
    outputs_dir = root / "outputs"
    internal_dir = root / ".analystools"

    for directory in [
        data_dir,
        raw_dir,
        curated_dir,
        analyses_dir,
        metrics_dir,
        reports_dir,
        charts_dir,
        outputs_dir,
        internal_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    config = ProjectConfig(name=name)

    config_file = root / "analystools.toml"

    config_file.write_text(
        f"""[project]
name = "{config.name}"
version = "{config.version}"

[storage]
warehouse = "{config.warehouse}"
metadata = "{config.metadata}"

[output]
directory = "{config.output_directory}"
""",
        encoding="utf-8",
    )

    metadata_store = MetadataStore(root / config.metadata)
    metadata_store.initialize()

    return Project(
        name=config.name,
        version=config.version,
        root=root,
        warehouse=root / config.warehouse,
        metadata=root / config.metadata,
        output_directory=root / config.output_directory,
    )