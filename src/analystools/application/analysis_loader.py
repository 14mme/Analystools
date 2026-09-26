from pathlib import Path

import yaml

from analystools.domain.analysis import AnalysisDefinition, AnalysisFile


def load_analysis(path: Path) -> AnalysisDefinition:
    if not path.exists():
        raise FileNotFoundError(
            f"Analysis Definition not found: {path}"
        )

    content = path.read_text(encoding="utf-8")

    if not content.strip():
        raise ValueError(
            f"Analysis Definition is empty: {path}"
        )

    data = yaml.safe_load(content)

    if not isinstance(data, dict):
        raise ValueError(
            f"Invalid analysis definition: {path}"
        )

    definition = AnalysisFile.model_validate(data)

    return definition.analysis