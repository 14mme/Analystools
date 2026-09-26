import typer

from analystools.application.analysis_service import (
    run_analysis,
)
from analystools.application.project_context import (
    discover_project,
)


def analyze(
    name: str = typer.Argument(
        help="Analysis name.",
    ),
) -> None:
    context = discover_project()

    result = run_analysis(
        context,
        name,
    )

    typer.echo(
        f"Analysis: {result.analysis_name}"
    )
    typer.echo(
        f"Dataset: {result.dataset}"
    )
    typer.echo(
        f"Run ID: {result.analysis_id}"
    )
    typer.echo(
        f"Execution: "
        f"{result.execution_time_ms:.2f} ms"
    )

    typer.echo("")
    _print_table(
        result.columns,
        result.rows,
    )

    typer.echo("")
    typer.echo("SQL:")
    typer.echo(result.sql)


def _print_table(
    columns: list[str],
    rows: list[tuple],
) -> None:
    if not columns:
        typer.echo("(no columns)")
        return

    string_rows = [
        [
            "" if value is None else str(value)
            for value in row
        ]
        for row in rows
    ]

    widths = [
        len(column)
        for column in columns
    ]

    for row in string_rows:
        for index, value in enumerate(row):
            widths[index] = max(
                widths[index],
                len(value),
            )

    header = " | ".join(
        column.ljust(widths[index])
        for index, column in enumerate(columns)
    )

    separator = "-+-".join(
        "-" * width
        for width in widths
    )

    typer.echo(header)
    typer.echo(separator)

    for row in string_rows:
        typer.echo(
            " | ".join(
                value.ljust(widths[index])
                for index, value in enumerate(row)
            )
        )