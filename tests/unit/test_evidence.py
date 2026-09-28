from analystools.analytics.insights.evidence import (
    collect_evidence,
)
from analystools.domain.analysis import (
    AnalysisResult,
)


def test_collect_evidence() -> None:
    result = AnalysisResult(
        analysis_id="run-001",
        analysis_name="revenue_by_category",
        dataset="sales",
        dimensions=["category"],
        metrics=["revenue", "profit"],
        columns=[
            "category",
            "revenue",
            "profit",
        ],
        rows=[
            ("Electronics", 125000, 25000),
            ("Furniture", 83000, 12000),
        ],
        sql=(
            'SELECT "category", '
            'SUM(revenue) AS "revenue", '
            'SUM(profit) AS "profit" '
            'FROM "sales";'
        ),
        execution_time_ms=12.5,
    )

    evidence = collect_evidence(result)

    assert evidence.run_id == "run-001"

    assert evidence.analysis_name == (
        "revenue_by_category"
    )

    assert evidence.dataset == "sales"

    assert evidence.dimensions == [
        "category"
    ]

    assert evidence.metrics == [
        "revenue",
        "profit",
    ]

    assert evidence.row_count == 2

    assert (
        evidence.values[0].dimensions[
            "category"
        ]
        == "Electronics"
    )

    assert (
        evidence.values[0].metrics[
            "revenue"
        ]
        == 125000
    )

    assert (
        evidence.values[0].metrics[
            "profit"
        ]
        == 25000
    )


def test_collect_evidence_uses_column_names() -> None:
    result = AnalysisResult(
        analysis_id="run-002",
        analysis_name="test",
        dataset="sales",
        dimensions=["category"],
        metrics=["revenue"],
        columns=[
            "revenue",
            "category",
        ],
        rows=[
            (100, "Electronics"),
        ],
        sql="SELECT ...",
        execution_time_ms=1.0,
    )

    evidence = collect_evidence(result)

    assert (
        evidence.values[0].dimensions[
            "category"
        ]
        == "Electronics"
    )

    assert (
        evidence.values[0].metrics[
            "revenue"
        ]
        == 100
    )