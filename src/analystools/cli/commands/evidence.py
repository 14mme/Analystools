import typer

from analystools.application.evidence_service import (
    get_evidence,
    list_evidence,
)
from analystools.application.project_context import (
    discover_project,
)


def list_command(
    analysis: str | None = typer.Option(
        None,
        "--analysis",
        "-a",
        help="Filter by analysis name.",
    ),
) -> None:
    context = discover_project()

    records = list_evidence(
        context,
        analysis_name=analysis,
    )

    if not records:
        typer.echo(
            "No evidence found."
        )
        return

    columns = [
        "evidence_id",
        "analysis_name",
        "dataset",
        "created_at",
    ]

    rows = [
        tuple(
            row[column]
            for column in columns
        )
        for row in records
    ]

    _print_table(
        columns,
        rows,
    )


def show(
    evidence_id: str = typer.Argument(
        ...,
        help="Evidence ID.",
    ),
) -> None:
    context = discover_project()

    evidence = get_evidence(
        context,
        evidence_id,
    )

    typer.echo(
        f"Evidence: {evidence.evidence_id}"
    )
    typer.echo(
        f"Run ID: {evidence.run_id}"
    )
    typer.echo(
        f"Analysis: {evidence.analysis_name}"
    )
    typer.echo(
        f"Dataset: {evidence.dataset}"
    )
    typer.echo(
        f"Dimensions: "
        f"{', '.join(evidence.dimensions)}"
    )
    typer.echo(
        f"Metrics: "
        f"{', '.join(evidence.metrics)}"
    )
    typer.echo(
        f"Rows: {evidence.row_count}"
    )
    typer.echo(
        f"Created: {evidence.created_at.isoformat()}"
    )

    typer.echo("")
    typer.echo("Values:")

    for index, value in enumerate(
        evidence.values,
        start=1,
    ):
        typer.echo(
            f"\n[{index}]"
        )

        if value.dimensions:
            typer.echo(
                "Dimensions:"
            )

            for key, item in (
                value.dimensions.items()
            ):
                typer.echo(
                    f"  {key}: {item}"
                )

        if value.metrics:
            typer.echo(
                "Metrics:"
            )

            for key, item in (
                value.metrics.items()
            ):
                typer.echo(
                    f"  {key}: {item}"
                )

    typer.echo("")
    typer.echo("SQL:")
    typer.echo(evidence.sql)


def _print_table(
    columns: list[str],
    rows: list[tuple],
) -> None:
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