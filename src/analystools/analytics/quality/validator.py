from dataclasses import dataclass

import polars as pl

from analystools.analytics.quality.rules import (
    QualityRule,
    Severity,
)


@dataclass(frozen=True)
class QualityResult:
    rule: str
    column: str | None
    severity: Severity
    passed: bool
    message: str


def check_not_null(
    dataframe: pl.DataFrame,
    column: str,
    severity: Severity = Severity.ERROR,
) -> QualityResult:
    if column not in dataframe.columns:
        return QualityResult(
            rule="not_null",
            column=column,
            severity=severity,
            passed=False,
            message=f"Column '{column}' does not exist.",
        )

    null_count = dataframe[column].null_count()

    return QualityResult(
        rule="not_null",
        column=column,
        severity=severity,
        passed=null_count == 0,
        message=(
            f"Column '{column}' contains "
            f"{null_count} null values."
        ),
    )


def check_unique(
    dataframe: pl.DataFrame,
    column: str,
    severity: Severity = Severity.ERROR,
) -> QualityResult:
    if column not in dataframe.columns:
        return QualityResult(
            rule="unique",
            column=column,
            severity=severity,
            passed=False,
            message=f"Column '{column}' does not exist.",
        )

    total = dataframe.height
    unique = dataframe[column].n_unique()

    return QualityResult(
        rule="unique",
        column=column,
        severity=severity,
        passed=total == unique,
        message=(
            f"Column '{column}' contains "
            f"{total - unique} duplicate values."
        ),
    )


def check_min(
    dataframe: pl.DataFrame,
    column: str,
    minimum: float,
    severity: Severity = Severity.ERROR,
) -> QualityResult:
    if column not in dataframe.columns:
        return QualityResult(
            rule="min",
            column=column,
            severity=severity,
            passed=False,
            message=f"Column '{column}' does not exist.",
        )

    minimum_value = dataframe[column].min()

    passed = (
        minimum_value is not None
        and minimum_value >= minimum
    )

    return QualityResult(
        rule="min",
        column=column,
        severity=severity,
        passed=passed,
        message=(
            f"Minimum value is {minimum_value}; "
            f"required >= {minimum}."
        ),
    )


def check_max(
    dataframe: pl.DataFrame,
    column: str,
    maximum: float,
    severity: Severity = Severity.ERROR,
) -> QualityResult:
    if column not in dataframe.columns:
        return QualityResult(
            rule="max",
            column=column,
            severity=severity,
            passed=False,
            message=f"Column '{column}' does not exist.",
        )

    maximum_value = dataframe[column].max()

    passed = (
        maximum_value is not None
        and maximum_value <= maximum
    )

    return QualityResult(
        rule="max",
        column=column,
        severity=severity,
        passed=passed,
        message=(
            f"Maximum value is {maximum_value}; "
            f"required <= {maximum}."
        ),
    )