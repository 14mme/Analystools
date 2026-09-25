import re

from analystools.analytics.metrics.registry import (
    MetricRegistry,
)
from analystools.infrastructure.storage.duckdb import (
    DuckDBStore,
)
from analystools.application.project_context import (
    ProjectContext,
)


_IDENTIFIER_PATTERN = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*$"
)


def calculate_metric(
    context: ProjectContext,
    metric_name: str,
    dataset_name: str,
    group_by: list[str] | None = None,
):
    registry = MetricRegistry(context)

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
        context.warehouse_path
    )

    return store.query(sql)