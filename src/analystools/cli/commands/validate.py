from pathlib import Path

import typer

from analystools.analytics.quality.checks import (
    run_basic_quality_checks,
)
from analystools.infrastructure.storage.parquet import (
    read_parquet,
)


def validate(
    dataset: str = typer.Argument(
        help="Dataset name.",
    ),
) -> None:
    path = (
        Path.cwd()
        / "data"
        / "curated"
        / f"{dataset}.parquet"
    )

    dataframe = read_parquet(path)

    report = run_basic_quality_checks(dataframe)

    print()
    print("Data Quality")
    print("=" * 60)

    for result in report.results:
        status = "PASS" if result.passed else "FAIL"

        print(
            f"[{status}] "
            f"{result.rule:<12} "
            f"{result.column:<25} "
            f"{result.message}"
        )

    print()
    print(
        f"Errors: {report.errors} | "
        f"Status: {'PASS' if report.passed else 'FAIL'}"
    )

    if not report.passed:
        raise typer.Exit(code=1)