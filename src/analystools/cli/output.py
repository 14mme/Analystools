from typing import Iterable


def print_success(message: str) -> None:
    print(f"[OK] {message}")


def print_error(message: str) -> None:
    print(f"[ERROR] {message}")


def print_table(
    rows: Iterable[dict],
) -> None:
    rows = list(rows)

    if not rows:
        print("No data found.")
        return

    columns = list(rows[0].keys())

    widths = {
        column: max(
            len(column),
            *(len(str(row[column])) for row in rows),
        )
        for column in columns
    }

    header = " | ".join(
        column.ljust(widths[column])
        for column in columns
    )

    separator = "-+-".join(
        "-" * widths[column]
        for column in columns
    )

    print(header)
    print(separator)

    for row in rows:
        print(
            " | ".join(
                str(row[column]).ljust(widths[column])
                for column in columns
            )
        )