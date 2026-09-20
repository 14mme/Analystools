import polars as pl

from analystools.analytics.quality.checks import (
    run_basic_quality_checks,
)


def test_quality_passes_without_nulls() -> None:
    dataframe = pl.DataFrame(
        {
            "id": [1, 2, 3],
            "value": [10, 20, 30],
        }
    )

    report = run_basic_quality_checks(dataframe)

    assert report.passed


def test_quality_reports_nulls_as_warning() -> None:
    dataframe = pl.DataFrame(
        {
            "id": [1, None, 3],
        }
    )

    report = run_basic_quality_checks(dataframe)

    assert len(report.results) == 1
    assert not report.results[0].passed
    assert report.results[0].severity.value == "warning"
    assert report.passed