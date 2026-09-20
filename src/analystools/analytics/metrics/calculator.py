import re
from pathlib import Path

from analystools.analytics.metrics.registry import (
    MetricRegistry,
)
from analystools.infrastructure.storage.duckdb import (
    DuckDBStore,
)


_IDENTIFIER_PATTERN = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*$"
)


def calculate_metric(
    project_root: Path,
    metric_name: str,
    dataset_name: str,
    group_by: list[str] | None = None,
):
    registry = MetricRegistry(
        project_root / "metrics"
    )

    metric = registry.get(metric_name)

    dimensions = group_by or []

    for dimension in dimensions:
        if not _IDENTIFIER_PATTERN.match(dimension):
            raise ValueError(
                f"Invalid column name: {dimension}"
            )

    select_parts = [
        *dimensions,
        f"{metric.expression} AS {metric.name}",
    ]

    sql = f"""
        SELECT
            {", ".join(select_parts)}
        FROM "{dataset_name}"
    """

    if dimensions:
        sql += f"""
            GROUP BY
                {", ".join(dimensions)}
        """

        sql += f"""
            ORDER BY
                {metric.name} DESC
        """

    store = DuckDBStore(
        project_root
        / ".analystools"
        / "warehouse.duckdb"
    )

    return store.query(sql)