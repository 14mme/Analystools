from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class DuplicateProfile:
    total_rows: int
    unique_rows: int
    duplicate_rows: int
    duplicate_percentage: float


def profile_duplicates(
    dataframe: pl.DataFrame,
) -> DuplicateProfile:
    total_rows = dataframe.height

    unique_rows = dataframe.unique().height

    duplicate_rows = total_rows - unique_rows

    duplicate_percentage = (
        duplicate_rows / total_rows * 100
        if total_rows > 0
        else 0.0
    )

    return DuplicateProfile(
        total_rows=total_rows,
        unique_rows=unique_rows,
        duplicate_rows=duplicate_rows,
        duplicate_percentage=duplicate_percentage,
    )