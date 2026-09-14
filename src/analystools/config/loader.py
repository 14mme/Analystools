import tomllib
from pathlib import Path

from analystools.config.schema import ProjectConfig


def load_config(path: Path) -> ProjectConfig:
    if not path.exists():
        raise FileNotFoundError(f"Project configuration not found: {path}")

    with path.open("rb") as file:
        data = tomllib.load(file)

    project = data.get("project", {})
    storage = data.get("storage", {})
    output = data.get("output", {})

    return ProjectConfig(
        name=project["name"],
        version=project.get("version", "0.1.0"),
        warehouse=Path(
            storage.get(
                "warehouse",
                ".analystools/warehouse.duckdb",
            )
        ),
        metadata=Path(
            storage.get(
                "metadata",
                ".analystools/metadata.db",
            )
        ),
        output_directory=Path(
            output.get(
                "directory",
                "outputs",
            )
        ),
    )