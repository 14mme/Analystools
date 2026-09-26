from pathlib import Path

import typer

from analystools.analytics.metrics.calculator import (
    calculate_metric,
)
from analystools.analytics.metrics.registry import (
    MetricRegistry,
)
from analystools.application.project_context import (
    discover_project,
)


def list_metrics() -> None:
    context = discover_project()
    registry = MetricRegistry(context)
    metrics = registry.list()

    if not metrics:
        print("No metrics registered.")
        return

    print()
    print("Metrics")
    print("=" * 80)

    for metric in metrics:
        print(
            f"{metric.name:<25} "
            f"{metric.format:<12} "
            f"{metric.description}"
        )


def show(
    name: str = typer.Argument(
        help="Metric name.",
    ),
) -> None:
    context = discover_project()
    registry = MetricRegistry(context)
    metric = registry.get(name)

    print()
    print(f"Metric: {metric.name}")
    print("=" * 60)
    print(f"Description : {metric.description}")
    print(f"Expression  : {metric.expression}")
    print(f"Format      : {metric.format}")


def calculate(
    name: str = typer.Argument(
        help="Metric name.",
    ),
    dataset: str = typer.Option(
        "--dataset",
        "-d",
        help="Dataset name.",
    ),
    group_by: list[str] | None = typer.Option(
        None,
        "--group-by",
        "-g",
        help="Column to group by.",
    ),
) -> None:
    context = discover_project()
    
    columns, rows = calculate_metric(
        context=context,
        metric_name=name,
        dataset_name=dataset,
        group_by=group_by,
    )

    _print_table(
        columns,
        rows,
    )


def _print_table(
    columns: list[str],
    rows: list[tuple],
) -> None:
    if not rows:
        print("No results.")
        return

    widths = []

    for index, column in enumerate(columns):
        values = [
            str(row[index])
            for row in rows
        ]

        widths.append(
            max(
                len(column),
                *(len(value) for value in values),
            )
        )

    print()

    print(
        " | ".join(
            column.ljust(widths[index])
            for index, column in enumerate(columns)
        )
    )

    print(
        "-+-".join(
            "-" * width
            for width in widths
        )
    )

    for row in rows:
        print(
            " | ".join(
                str(value).ljust(widths[index])
                for index, value in enumerate(row)
            )
        )