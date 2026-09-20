import polars as pl
import pytest

from analystools.analytics.profiling.cardinality import (
    profile_cardinality,
)
from analystools.analytics.profiling.duplicates import (
    profile_duplicates,
)
from analystools.analytics.profiling.missing import (
    profile_missing,
)
from analystools.analytics.profiling.schema import (
    infer_schema,
)


def test_schema_inference() -> None:
    dataframe = pl.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "revenue": [100.0, 200.0, 300.0],
            "category": ["A", "B", "A"],
        }
    )

    result = infer_schema(dataframe)

    semantic_types = {
        item.name: item.semantic_type
        for item in result
    }

    assert semantic_types["customer_id"] == "identifier"
    assert semantic_types["revenue"] == "numeric"
    assert semantic_types["category"] == "categorical"


def test_missing_profile() -> None:
    dataframe = pl.DataFrame(
        {
            "value": [1, None, 3],
        }
    )

    result = profile_missing(dataframe)

    assert result[0].missing_count == 1
    assert result[0].missing_percentage == pytest.approx(
        100 / 3
    )


def test_duplicate_profile() -> None:
    dataframe = pl.DataFrame(
        {
            "id": [1, 1, 2],
        }
    )

    result = profile_duplicates(dataframe)

    assert result.total_rows == 3
    assert result.unique_rows == 2
    assert result.duplicate_rows == 1


def test_cardinality_profile() -> None:
    dataframe = pl.DataFrame(
        {
            "category": ["A", "A", "B", "B"],
        }
    )

    result = profile_cardinality(dataframe)

    assert result[0].unique_count == 2
    assert result[0].unique_percentage == pytest.approx(50.0)