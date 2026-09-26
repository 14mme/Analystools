import typer

from analystools.application.project_context import (
    discover_project
)
from analystools.infrastructure.storage.sqlite import (
    SQLiteStore
)


def list_runs() -> None:
    context = discover_project()

    store = SQLiteStore(
        context.metadata_path
    )

    store.initialize()

    runs = store.list_runs()

    if not runs:
        typer.echo("No analysis runs found.")
        return

    columns = [
        "run_id",
        "analysis_name",
        "dataset",
        "status",
        "execution_time_ms",
        "created_at",
    ]

    rows = [
        tuple(row[column] for column in columns)
        for row in runs
    ]

    _print_table(columns, rows)


def _print_table(
        columns: list[str],
        rows: list[tuple],
) -> None:
    widths = [
        len(column)
        for column in columns
    ]

    string_rows = []

    for row in rows:
        values = [
            "" if value is None else str(value)
            for value in row
        ]

        string_rows.append(values)

        for index, value in enumerate(values):
            widths[index] = max(
                widths[index],
                len(value),
            )

    typer.echo(
        " | ".join(
            column.ljust(widths[index])
            for index, column in enumerate(columns)
        )
    )

    typer.echo(
        "-+-".join(
            "-" * width
            for width in widths
        )
    )

    for row in string_rows:
        typer.echo(
            " | ".join(
                value.ljust(widths[index])
                for index, value in enumerate(row)
            )
        )