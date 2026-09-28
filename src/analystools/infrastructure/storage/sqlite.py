from pathlib import Path
import sqlite3
import json


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

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS evidence (
                    evidence_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    analysis_name TEXT NOT NULL,
                    dataset TEXT NOT NULL,
                    dimensions TEXT NOT NULL,
                    metrics TEXT NOT NULL,
                    sql TEXT NOT NULL,
                    values_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (run_id)
                        REFERENCES runs(run_id)
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

    def record_evidence(
        self,
        evidence_id: str,
        run_id: str,
        analysis_name: str,
        dataset: str,
        dimensions: list[str],
        metrics: list[str],
        sql: str,
        values: list[dict],
        created_at: str,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO evidence (
                    evidence_id,
                    run_id,
                    analysis_name,
                    dataset,
                    dimensions,
                    metrics,
                    sql,
                    values_json,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    evidence_id,
                    run_id,
                    analysis_name,
                    dataset,
                    json.dumps(dimensions),
                    json.dumps(metrics),
                    sql,
                    json.dumps(
                        values,
                        default=str,
                    ),
                    created_at,
                ),
            )

            connection.commit()

    def get_evidence(
        self,
        evidence_id: str,
    ) -> sqlite3.Row | None:
        with self.connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    evidence_id,
                    run_id,
                    analysis_name,
                    dataset,
                    dimensions,
                    metrics,
                    sql,
                    values_json,
                    created_at
                FROM evidence
                WHERE evidence_id = ?
                """,
                (evidence_id,),
            )

            return cursor.fetchone()

    def list_evidence(
        self,
        analysis_name: str | None = None,
    ) -> list[sqlite3.Row]:
        with self.connect() as connection:
            if analysis_name:
                cursor = connection.execute(
                    """
                    SELECT
                        evidence_id,
                        run_id,
                        analysis_name,
                        dataset,
                        dimensions,
                        metrics,
                        created_at
                    FROM evidence
                    WHERE analysis_name = ?
                    ORDER BY created_at DESC
                    """,
                    (analysis_name,),
                )
            else:
                cursor = connection.execute(
                    """
                    SELECT
                        evidence_id,
                        run_id,
                        analysis_name,
                        dataset,
                        dimensions,
                        metrics,
                        created_at
                    FROM evidence
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