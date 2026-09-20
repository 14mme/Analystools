from pathlib import Path

from analystools.analytics.profiling.cardinality import (
    profile_cardinality,
)
from analystools.analytics.profiling.distributions import (
    profile_numeric_distributions,
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
from analystools.domain.profile import ProfileResult
from analystools.infrastructure.storage.parquet import (
    read_parquet,
)


def profile_dataset(
    project_root: Path,
    dataset_name: str,
) -> ProfileResult:
    parquet_path = (
        project_root
        / "data"
        / "curated"
        / f"{dataset_name}.parquet"
    )

    dataframe = read_parquet(parquet_path)

    return ProfileResult(
        rows=dataframe.height,
        columns=dataframe.width,
        schema=infer_schema(dataframe),
        missing=profile_missing(dataframe),
        duplicates=profile_duplicates(dataframe),
        cardinality=profile_cardinality(dataframe),
        distributions=profile_numeric_distributions(dataframe),
    )