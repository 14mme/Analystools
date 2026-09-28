from analystools.analytics.insights.detector import (
    detect_insights,
)
from analystools.domain.evidence import (
    Evidence,
    EvidenceValue,
)


def make_evidence() -> Evidence:
    return Evidence(
        evidence_id="evidence-001",
        run_id="run-001",
        analysis_name="revenue_by_category",
        dataset="sales",
        dimensions=["category"],
        metrics=[
            "revenue",
            "profit",
            "profit_margin",
        ],
        sql="SELECT ...",
        values=[
            EvidenceValue(
                dimensions={
                    "category": "Electronics"
                },
                metrics={
                    "revenue": 700,
                    "profit": 140,
                    "profit_margin": 0.20,
                },
            ),
            EvidenceValue(
                dimensions={
                    "category": "Furniture"
                },
                metrics={
                    "revenue": 200,
                    "profit": 20,
                    "profit_margin": 0.10,
                },
            ),
            EvidenceValue(
                dimensions={
                    "category": "Clothing"
                },
                metrics={
                    "revenue": 100,
                    "profit": 5,
                    "profit_margin": 0.05,
                },
            ),
        ],
    )


def test_detect_revenue_concentration() -> None:
    evidence = make_evidence()

    insights = detect_insights(
        evidence
    )

    concentration = [
        item
        for item in insights
        if item.type == "concentration"
    ]

    assert len(concentration) == 1

    assert (
        "Electronics"
        in concentration[0].title
    )


def test_detect_margin_difference() -> None:
    evidence = make_evidence()

    insights = detect_insights(
        evidence
    )

    margin_insights = [
        item
        for item in insights
        if item.type == "margin_difference"
    ]

    assert len(margin_insights) == 1

    assert (
        "Electronics"
        in margin_insights[0].title
    )


def test_insight_references_evidence() -> None:
    evidence = make_evidence()

    insights = detect_insights(
        evidence
    )

    assert insights

    for insight in insights:
        assert (
            insight.evidence_id
            == evidence.evidence_id
        )