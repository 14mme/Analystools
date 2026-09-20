from dataclasses import dataclass

import polars as pl


@dataclass(frozen=True)
class ColumnSchema:
    name: str
    dtype: str
    semantic_type: str
    nullable: bool


def infer_semantic_type(
    name: str,
    dtype: pl.DataType,
) -> str:
    name_lower = name.lower()

    if dtype.is_temporal():
        return "datetime"

    if dtype.is_numeric():
        if any(
            keyword in name_lower
            for keyword in (
                "id",
                "code",
                "zip",
                "postal",
            )
        ):
            return "identifier"

        return "numeric"

    if dtype == pl.Boolean:
        return "boolean"

    if dtype == pl.String:
        if any(
            keyword in name_lower
            for keyword in (
                "id",
                "code",
                "uuid",
                "key",
            )
        ):
            return "identifier"

        return "categorical"

    return "other"


def infer_schema(
    dataframe: pl.DataFrame,
) -> list[ColumnSchema]:
    result: list[ColumnSchema] = []

    for name, dtype in dataframe.schema.items():
        nullable = dataframe[name].null_count() > 0

        result.append(
            ColumnSchema(
                name=name,
                dtype=str(dtype),
                semantic_type=infer_semantic_type(
                    name,
                    dtype,
                ),
                nullable=nullable,
            )
        )

    return result