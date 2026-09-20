from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class CardinalityProfile:
    column: str
    unique_count: int
    unique_percentage: float


def profile_cardinality(
    dataframe: pl.DataFrame,
) -> list[CardinalityProfile]:
    total_rows = dataframe.height

    result: list[CardinalityProfile] = []

    for column in dataframe.columns:
        unique_count = dataframe[column].n_unique()

        percentage = (
            unique_count / total_rows * 100
            if total_rows > 0
            else 0.0
        )

        result.append(
            CardinalityProfile(
                column=column,
                unique_count=unique_count,
                unique_percentage=percentage,
            )
        )

    return result