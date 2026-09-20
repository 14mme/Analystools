from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class NumericDistribution:
    column: str
    count: int
    mean: float | None
    median: float | None
    minimum: float | None
    maximum: float | None
    standard_deviation: float | None


def profile_numeric_distributions(
    dataframe: pl.DataFrame,
) -> list[NumericDistribution]:
    result: list[NumericDistribution] = []

    for column, dtype in dataframe.schema.items():
        if not dtype.is_numeric():
            continue

        series = dataframe[column]

        result.append(
            NumericDistribution(
                column=column,
                count=series.len(),
                mean=_to_float(series.mean()),
                median=_to_float(series.median()),
                minimum=_to_float(series.min()),
                maximum=_to_float(series.max()),
                standard_deviation=_to_float(
                    series.std()
                ),
            )
        )

    return result


def _to_float(
    value: object,
) -> float | None:
    if value is None:
        return None

    return float(value)