import csv
from pathlib import Path

import typer

from analystools.application.query_service import (
    execute_query,
)
from analystools.application.project_context import (
    discover_project,
)


def query(
    sql_file: Path = typer.Argument(
        exists=True,
        readable=True,
        help="SQL file to execute.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional CSV output file.",
    ),
) -> None:
    context = discover_project()
    columns, rows = execute_query(
        context=context,
        sql_file=sql_file,
    )

    _print_table(
        columns,
        rows,
    )

    if output:
        _write_csv(
            output,
            columns,
            rows,
        )

        print()
        print(
            f"[OK] Result exported to {output}"
        )


def _print_table(
    columns: list[str],
    rows: list[tuple],
) -> None:
    if not rows:
        print("Query returned no rows.")
        return

    print()

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

    header = " | ".join(
        column.ljust(widths[index])
        for index, column in enumerate(columns)
    )

    separator = "-+-".join(
        "-" * width
        for width in widths
    )

    print(header)
    print(separator)

    for row in rows:
        print(
            " | ".join(
                str(value).ljust(widths[index])
                for index, value in enumerate(row)
            )
        )

    print()
    print(f"{len(rows):,} row(s)")


def _write_csv(
    path: Path,
    columns: list[str],
    rows: list[tuple],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.writer(file)

        writer.writerow(columns)
        writer.writerows(rows)