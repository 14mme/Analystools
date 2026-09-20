import tomllib
from pathlib import Path

from analystools.domain.metric import Metric


class MetricRegistry:
    def __init__(self, metrics_directory: Path) -> None:
        self.metrics_directory = metrics_directory

    def list(self) -> list[Metric]:
        if not self.metrics_directory.exists():
            return []

        metrics: list[Metric] = []

        for path in sorted(
            self.metrics_directory.glob("*.toml")
        ):
            metrics.append(self._load_file(path))

        return metrics

    def get(self, name: str) -> Metric:
        path = self.metrics_directory / f"{name}.toml"

        if not path.exists():
            raise FileNotFoundError(
                f"Metric '{name}' not found at {path}"
            )

        return self._load_file(path)

    def _load_file(self, path: Path) -> Metric:
        with path.open("rb") as file:
            data = tomllib.load(file)

        metric = data.get("metric")

        if not metric:
            raise ValueError(
                f"Invalid metric definition: {path}"
            )

        return Metric(
            name=metric["name"],
            description=metric.get(
                "description",
                "",
            ),
            expression=metric["expression"],
            format=metric.get(
                "format",
                "number",
            ),
        )