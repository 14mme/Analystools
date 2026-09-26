from pathlib import Path
import sqlite3


class SQLiteStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    analysis_name TEXT NOT NULL,
                    dataset TEXT NOT NULL,
                    status TEXT NOT NULL,
                    execution_time_ms REAL NOT NULL,
                    sql TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.commit()

    def record_run(
        self,
        run_id: str,
        analysis_name: str,
        dataset: str,
        status: str,
        execution_time_ms: float,
        sql: str,
        created_at: str,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO runs (
                    run_id,
                    analysis_name,
                    dataset,
                    status,
                    execution_time_ms,
                    sql,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    analysis_name,
                    dataset,
                    status,
                    execution_time_ms,
                    sql,
                    created_at,
                ),
            )

            connection.commit()

    def list_runs(self) -> list[sqlite3.Row]:
        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    run_id,
                    analysis_name,
                    dataset,
                    status,
                    execution_time_ms,
                    created_at
                FROM runs
                ORDER BY created_at DESC
                """
            )

            return cursor.fetchall()


class MetadataStore(SQLiteStore):
    """
    Backward-compatible metadata store.

    Existing application services may still import
    MetadataStore. Keep this alias until those services
    are migrated to SQLiteStore explicitly.
    """

    pass