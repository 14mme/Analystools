import tomllib
from pathlib import Path

from analystools.config.schema import ProjectConfig


def load_config(path: Path) -> ProjectConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("rb") as file:
        data = tomllib.load(file)

    return ProjectConfig.model_validate(data)