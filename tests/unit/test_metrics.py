from pathlib import Path

from analystools.analytics.metrics.registry import (
    MetricRegistry,
)


def test_metric_registry(tmp_path: Path) -> None:
    metrics_directory = tmp_path / "metrics"
    metrics_directory.mkdir()

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

    registry = MetricRegistry(
        metrics_directory
    )

    metric = registry.get("revenue")

    assert metric.name == "revenue"
    assert metric.expression == "SUM(revenue)"
    assert metric.format == "currency"


def test_metric_registry_list(tmp_path: Path) -> None:
    metrics_directory = tmp_path / "metrics"
    metrics_directory.mkdir()

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

    registry = MetricRegistry(
        metrics_directory
    )

    metrics = registry.list()

    assert len(metrics) == 2
    assert {
        metric.name
        for metric in metrics
    } == {
        "revenue",
        "profit",
    }