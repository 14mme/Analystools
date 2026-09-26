from pathlib import Path

import typer

from analystools.application.dataset_service import (
    list_datasets,
    register_dataset,
)
from analystools.application.project_context import (
    discover_project,
)
from analystools.cli.output import print_success, print_table


def add(
    file: Path = typer.Argument(
        exists=True,
        readable=True,
        help="CSV or Parquet dataset.",
    ),
    name: str = typer.Option(
        "--name",
        "-n",
        help="Dataset name.",
    ),
) -> None:
    context = discover_project()

    dataset = register_dataset(
        context=context,
        source=file,
        name=name,
    )

    print_success(
        f"Dataset '{dataset.name}' registered."
    )

    print(f"Rows: {dataset.rows:,}")
    print(f"Columns: {dataset.columns}")
    print(f"Parquet: {dataset.parquet_path}")


def list_command() -> None:
    context = discover_project()
    rows = list_datasets(context)
    print_table(rows)