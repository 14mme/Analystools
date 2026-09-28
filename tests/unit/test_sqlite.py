from pathlib import Path

from analystools.infrastructure.storage.sqlite import (
    SQLiteStore,
)


def test_sqlite_initialize(
    tmp_path: Path,
) -> None:
    store = SQLiteStore(
        tmp_path / "metadata.db"
    )

    store.initialize()

    with store.connect() as connection:
        runs = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    table_names = {
        row["name"]
        for row in runs
    }

    assert "runs" in table_names
    assert "evidence" in table_names