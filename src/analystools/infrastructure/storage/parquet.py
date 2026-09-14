from pathlib import Path

import polars as pl


def write_parquet(
    dataframe: pl.DataFrame,
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.write_parquet(path)


def read_parquet(path: Path) -> pl.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Parquet file not found: {path}")

    return pl.read_parquet(path)