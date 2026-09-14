from pathlib import Path

import polars as pl


def load_csv(path: Path) -> pl.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected CSV file, got: {path}")

    return pl.read_csv(path)