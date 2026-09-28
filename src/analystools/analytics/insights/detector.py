from datetime import datetime, timezone
from uuid import uuid4

from analystools.analytics.insights.rules import (
    CONCENTRATION_THRESHOLD,
    HIGH_MARGIN_DIFFERENCE,
)
from analystools.domain.evidence import Evidence
from analystools.domain.insight import (
    Insight,
    InsightEvidence,
)


def detect_concentration(
    evidence: Evidence,
    metric: str,
) -> list[Insight]:
    if not evidence.values:
        return []

    totals: list[tuple[object, float]] = []

    for value in evidence.values:
        raw_value = value.metrics.get(metric)

        if raw_value is None:
            continue

        try:
            numeric_value = float(raw_value)
        except (TypeError, ValueError):
            continue

        dimension_value = next(
            iter(value.dimensions.values()),
            "unknown",
        )

        totals.append(
            (
                dimension_value,
                numeric_value,
            )
        )

    if not totals:
        return []

    total = sum(
        value
        for _, value in totals
    )

    if total == 0:
        return []

    insights: list[Insight] = []

    for dimension_value, value in totals:
        share = value / total

        if share < CONCENTRATION_THRESHOLD:
            continue

        evidence_item = next(
            item
            for item in evidence.values
            if next(
                iter(item.dimensions.values()),
                "unknown",
            )
            == dimension_value
        )

        insights.append(
            Insight(
                insight_id=str(uuid4()),
                evidence_id=evidence.evidence_id,
                analysis_name=evidence.analysis_name,
                type="concentration",
                title=(
                    f"{dimension_value} represents "
                    f"{share:.1%} of {metric}"
                ),
                description=(
                    f"{dimension_value} contributes "
                    f"{share:.1%} of total {metric}. "
                    f"The concentration threshold is "
                    f"{CONCENTRATION_THRESHOLD:.0%}."
                ),
                importance="high",
                evidence=[
                    InsightEvidence(
                        evidence_id=evidence.evidence_id,
                        dimensions=(
                            evidence_item.dimensions
                        ),
                        metrics=(
                            evidence_item.metrics
                        ),
                    )
                ],
                created_at=datetime.now(
                    timezone.utc
                ),
            )
        )

    return insights

def detect_margin_difference(
    evidence: Evidence,
    metric: str = "profit_margin",
) -> list[Insight]:
    if len(evidence.values) < 2:
        return []

    candidates = []

    for value in evidence.values:
        raw_margin = value.metrics.get(metric)

        if raw_margin is None:
            continue

        try:
            margin = float(raw_margin)
        except (TypeError, ValueError):
            continue

        dimension_value = next(
            iter(value.dimensions.values()),
            "unknown",
        )

        candidates.append(
            (
                dimension_value,
                margin,
                value,
            )
        )

    if len(candidates) < 2:
        return []

    highest = max(
        candidates,
        key=lambda item: item[1],
    )

    lowest = min(
        candidates,
        key=lambda item: item[1],
    )

    difference = (
        highest[1] - lowest[1]
    )

    if difference < HIGH_MARGIN_DIFFERENCE:
        return []

    return [
        Insight(
            insight_id=str(uuid4()),
            evidence_id=evidence.evidence_id,
            analysis_name=evidence.analysis_name,
            type="margin_difference",
            title=(
                f"{highest[0]} has a "
                f"{difference:.1%} higher profit margin "
                f"than {lowest[0]}"
            ),
            description=(
                f"{highest[0]} has a profit margin of "
                f"{highest[1]:.1%}, while "
                f"{lowest[0]} has "
                f"{lowest[1]:.1%}. "
                f"The difference is "
                f"{difference:.1%}."
            ),
            importance="medium",
            evidence=[
                InsightEvidence(
                    evidence_id=evidence.evidence_id,
                    dimensions=highest[2].dimensions,
                    metrics=highest[2].metrics,
                ),
                InsightEvidence(
                    evidence_id=evidence.evidence_id,
                    dimensions=lowest[2].dimensions,
                    metrics=lowest[2].metrics,
                ),
            ],
            created_at=datetime.now(
                timezone.utc
            ),
        )
    ]

def detect_insights(
    evidence: Evidence,
) -> list[Insight]:
    insights: list[Insight] = []

    if "revenue" in evidence.metrics:
        insights.extend(
            detect_concentration(
                evidence,
                metric="revenue",
            )
        )

    if "profit_margin" in evidence.metrics:
        insights.extend(
            detect_margin_difference(
                evidence
            )
        )

    return insights