from dataclasses import dataclass

from analystools.analytics.profiling.cardinality import (
    CardinalityProfile,
)
from analystools.analytics.profiling.distributions import (
    NumericDistribution,
)
from analystools.analytics.profiling.missing import (
    MissingProfile,
)
from analystools.analytics.profiling.schema import (
    ColumnSchema,
)
from analystools.analytics.profiling.duplicates import (
    DuplicateProfile,
)


@dataclass(frozen=True)
class ProfileResult:
    rows: int
    columns: int
    schema: list[ColumnSchema]
    missing: list[MissingProfile]
    duplicates: DuplicateProfile
    cardinality: list[CardinalityProfile]
    distributions: list[NumericDistribution]