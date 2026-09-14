from pathlib import Path

import polars as pl


def load_parquet(path: Path) -> pl.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Parquet file not found: {path}")

    return pl.read_parquet(path)