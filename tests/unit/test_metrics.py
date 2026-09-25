from pathlib import Path

from analystools.analytics.metrics.registry import (
    MetricRegistry,
)
from analystools.application.project_context import discover_project

def create_project(tmp_path: Path) -> tuple[Path, object]:
    project_root = tmp_path / "ecommerce"
    project_root.mkdir()

    metrics_directory = project_root / "metrics"
    metrics_directory.mkdir()

    config = project_root / "analystools.toml"
    config.write_text(
"""
[project]
name = "ecommerce"
version = "0.1.0"

[storage]
warehouse = ".analystools/warehouse.duckdb"
metadata = ".analystools/metadata.db"

[output]
directory = "outputs"
""".strip(),
        encoding="utf-8",
    )

    context = discover_project(project_root)
    return metrics_directory, context

def test_metric_registry(tmp_path: Path) -> None:
    metrics_directory, context = create_project(tmp_path)
    metric_file = metrics_directory / "revenue.toml"
    metric_file.write_text(
        """
[metric]
name = "revenue"
description = "Total revenue"
expression = "SUM(revenue)"
format = "currency"
""".strip(),
        encoding="utf-8",
    )

    registry = MetricRegistry(context)

    metric = registry.get("revenue")

    assert metric.name == "revenue"
    assert metric.description == "Total revenue"
    assert metric.expression == "SUM(revenue)"
    assert metric.format == "currency"


def test_metric_registry_list(tmp_path: Path) -> None:
    metrics_directory, context = create_project(tmp_path)

    (metrics_directory / "revenue.toml").write_text(
        """
[metric]
name = "revenue"
expression = "SUM(revenue)"
""".strip(),
        encoding="utf-8",
    )

    (metrics_directory / "profit.toml").write_text(
        """
[metric]
name = "profit"
expression = "SUM(profit)"
""".strip(),
        encoding="utf-8",
    )

    registry = MetricRegistry(context)

    metrics = registry.list()

    names = {metric.name for metric in metrics}
    
    assert names == {"revenue", "profit"}