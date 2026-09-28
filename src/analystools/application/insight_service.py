import json

from analystools.analytics.insights.detector import (
    detect_insights,
)
from analystools.application.evidence_service import (
    get_evidence,
)
from analystools.application.project_context import (
    ProjectContext,
)
from analystools.domain.insight import Insight
from analystools.infrastructure.storage.sqlite import (
    SQLiteStore,
)


def generate_insights(
    context: ProjectContext,
    evidence_id: str,
) -> list[Insight]:
    evidence = get_evidence(
        context,
        evidence_id,
    )

    insights = detect_insights(
        evidence
    )

    store = SQLiteStore(
        context.metadata_path
    )

    store.initialize()

    for insight in insights:
        store.record_insight(
            insight_id=insight.insight_id,
            evidence_id=insight.evidence_id,
            analysis_name=insight.analysis_name,
            insight_type=insight.type,
            title=insight.title,
            description=insight.description,
            importance=insight.importance,
            evidence=[
                item.model_dump(mode="json")
                for item in insight.evidence
            ],
            created_at=(
                insight.created_at.isoformat()
            ),
        )

    return insights


def list_insights(
    context: ProjectContext,
) -> list:
    store = SQLiteStore(
        context.metadata_path
    )

    store.initialize()

    return store.list_insights()