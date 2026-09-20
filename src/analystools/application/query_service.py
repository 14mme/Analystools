from pathlib import Path

from analystools.infrastructure.storage.duckdb import (
    DuckDBStore,
)


def execute_query(
    project_root: Path,
    sql_file: Path,
) -> tuple[list[str], list[tuple]]:
    if not sql_file.exists():
        raise FileNotFoundError(
            f"SQL file not found: {sql_file}"
        )

    sql = sql_file.read_text(
        encoding="utf-8"
    ).strip()

    if not sql:
        raise ValueError(
            f"SQL file is empty: {sql_file}"
        )

    store = DuckDBStore(
        project_root
        / ".analystools"
        / "warehouse.duckdb"
    )

    return store.query(sql)