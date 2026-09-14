import hashlib
from datetime import UTC, datetime
from pathlib import Path

import polars as pl

from analystools.domain.dataset import Dataset
from analystools.infrastructure.loader.csv import load_csv
from analystools.infrastructure.loader.parquet import load_parquet
from analystools.infrastructure.storage.duckdb import DuckDBStore
from analystools.infrastructure.storage.parquet import write_parquet
from analystools.infrastructure.storage.sqlite import MetadataStore


def calculate_file_hash(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            digest.update(chunk)

    return digest.hexdigest()


def load_dataset(path: Path) -> pl.DataFrame:
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return load_csv(path)

    if suffix == ".parquet":
        return load_parquet(path)

    raise ValueError(
        f"Unsupported dataset format: {suffix}. "
        "Supported formats: CSV, Parquet."
    )


def register_dataset(
    project_root: Path,
    source: Path,
    name: str,
) -> Dataset:
    source = source.resolve()

    if not source.exists():
        raise FileNotFoundError(f"Dataset not found: {source}")

    dataframe = load_dataset(source)

    parquet_path = (
        project_root
        / "data"
        / "curated"
        / f"{name}.parquet"
    )

    write_parquet(dataframe, parquet_path)

    metadata = MetadataStore(
        project_root / ".analystools" / "metadata.db"
    )

    metadata.initialize()

    dataset = Dataset(
        name=name,
        source=source,
        parquet_path=parquet_path,
        rows=dataframe.height,
        columns=dataframe.width,
        created_at=datetime.now(UTC),
        source_hash=calculate_file_hash(source),
    )

    with metadata.connect() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO datasets (
                name,
                source_path,
                parquet_path,
                rows,
                columns,
                source_hash,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dataset.name,
                str(dataset.source),
                str(dataset.parquet_path),
                dataset.rows,
                dataset.columns,
                dataset.source_hash,
                dataset.created_at.isoformat(),
            ),
        )

    duckdb_store = DuckDBStore(
        project_root / ".analystools" / "warehouse.duckdb"
    )

    duckdb_store.register_parquet(
        name,
        parquet_path,
    )

    return dataset


def list_datasets(project_root: Path) -> list[dict]:
    metadata = MetadataStore(
        project_root / ".analystools" / "metadata.db"
    )

    metadata.initialize()

    with metadata.connect() as connection:
        rows = connection.execute(
            """
            SELECT
                name,
                rows,
                columns,
                created_at
            FROM datasets
            ORDER BY name
            """
        ).fetchall()

    return [dict(row) for row in rows]