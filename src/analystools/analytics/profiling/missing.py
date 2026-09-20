from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class MissingProfile:
    column: str
    missing_count: int
    missing_percentage: float


def profile_missing(
    dataframe: pl.DataFrame,
) -> list[MissingProfile]:
    total_rows = dataframe.height

    result: list[MissingProfile] = []

    for column in dataframe.columns:
        missing_count = dataframe[column].null_count()

        percentage = (
            missing_count / total_rows * 100
            if total_rows > 0
            else 0.0
        )

        result.append(
            MissingProfile(
                column=column,
                missing_count=missing_count,
                missing_percentage=percentage,
            )
        )

    return result