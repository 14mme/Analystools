from dataclasses import dataclass

import polars as pl

from analystools.analytics.quality.rules import Severity
from analystools.analytics.quality.validator import (
    QualityResult,
    check_not_null,
    check_unique,
)


@dataclass(frozen=True)
class QualityReport:
    results: list[QualityResult]

    @property
    def passed(self) -> bool:
        return all(
            result.passed
            for result in self.results
            if result.severity == Severity.ERROR
        )

    @property
    def errors(self) -> int:
        return sum(
            1
            for result in self.results
            if not result.passed
            and result.severity == Severity.ERROR
        )


def run_basic_quality_checks(
    dataframe: pl.DataFrame,
) -> QualityReport:
    results: list[QualityResult] = []

    for column in dataframe.columns:
        results.append(
            check_not_null(
                dataframe,
                column,
                severity=Severity.WARNING,
            )
        )

    return QualityReport(results=results)


def check_identifier(
    dataframe: pl.DataFrame,
    column: str,
) -> QualityResult:
    return check_unique(
        dataframe,
        column,
        severity=Severity.ERROR,
    )