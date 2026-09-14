from pathlib import Path

import duckdb


class DuckDBStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(str(self.path))

    def register_parquet(
        self,
        table_name: str,
        parquet_path: Path,
    ) -> None:
        if not parquet_path.exists():
            raise FileNotFoundError(
                f"Parquet file not found: {parquet_path}"
            )

        with self.connect() as connection:
            connection.execute(
                f"""
                CREATE OR REPLACE VIEW "{table_name}"
                AS SELECT * FROM read_parquet(?)
                """,
                [str(parquet_path)],
            )

    def query(self, sql: str):
        with self.connect() as connection:
            return connection.execute(sql).fetchdf()