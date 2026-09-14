from pathlib import Path

import typer

from analystools.application.dataset_service import (
    list_datasets,
    register_dataset,
)
from analystools.cli.output import print_success, print_table


def add(
    file: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="CSV or Parquet dataset.",
    ),
    name: str = typer.Option(
        ...,
        "--name",
        "-n",
        help="Dataset name.",
    ),
) -> None:
    project_root = Path.cwd()

    dataset = register_dataset(
        project_root=project_root,
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
    rows = list_datasets(Path.cwd())
    print_table(rows)