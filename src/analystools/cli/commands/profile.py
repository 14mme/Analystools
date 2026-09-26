from pathlib import Path

import typer

from analystools.application.profile_service import (
    profile_dataset,
)
from analystools.application.project_context import (
    discover_project,
)


def profile(
    dataset: str = typer.Argument(
        help="Dataset name.",
    ),
) -> None:
    context = discover_project()

    result = profile_dataset(
        context=context,
        dataset_name=dataset,
    )

    print()
    print("Dataset Profile")
    print("=" * 60)

    print(f"Rows    : {result.rows:,}")
    print(f"Columns : {result.columns}")

    print()
    print("Schema")
    print("-" * 60)

    for column in result.schema:
        nullable = "yes" if column.nullable else "no"

        print(
            f"{column.name:<25} "
            f"{column.dtype:<15} "
            f"{column.semantic_type:<15} "
            f"nullable={nullable}"
        )

    print()
    print("Missing Values")
    print("-" * 60)

    for item in result.missing:
        if item.missing_count > 0:
            print(
                f"{item.column:<25} "
                f"{item.missing_count:>8,} "
                f"({item.missing_percentage:.2f}%)"
            )

    print()
    print("Duplicates")
    print("-" * 60)

    duplicate = result.duplicates

    print(f"Total rows      : {duplicate.total_rows:,}")
    print(f"Unique rows     : {duplicate.unique_rows:,}")
    print(f"Duplicate rows  : {duplicate.duplicate_rows:,}")
    print(
        f"Duplicate rate  : "
        f"{duplicate.duplicate_percentage:.2f}%"
    )

    print()
    print("Numeric Distributions")
    print("-" * 60)

    for item in result.distributions:
        print(
            f"{item.column:<20} "
            f"mean={_format(item.mean):>12} "
            f"median={_format(item.median):>12} "
            f"min={_format(item.minimum):>12} "
            f"max={_format(item.maximum):>12}"
        )


def _format(
    value: float | None,
) -> str:
    if value is None:
        return "N/A"

    return f"{value:,.2f}"