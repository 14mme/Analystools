import json

from analystools.application.project_context import (
    ProjectContext,
)
from analystools.analytics.insights.evidence import (
    collect_evidence,
)
from analystools.domain.analysis import AnalysisResult
from analystools.domain.evidence import Evidence
from analystools.infrastructure.storage.sqlite import (
    SQLiteStore,
)


def save_evidence(
    context: ProjectContext,
    result: AnalysisResult,
) -> Evidence:
    evidence = collect_evidence(result)

    store = SQLiteStore(
        context.metadata_path
    )

    store.initialize()

    values = [
        {
            "dimensions": item.dimensions,
            "metrics": item.metrics,
        }
        for item in evidence.values
    ]

    store.record_evidence(
        evidence_id=evidence.evidence_id,
        run_id=evidence.run_id,
        analysis_name=evidence.analysis_name,
        dataset=evidence.dataset,
        dimensions=evidence.dimensions,
        metrics=evidence.metrics,
        sql=evidence.sql,
        values=values,
        created_at=evidence.created_at.isoformat(),
    )

    return evidence


def get_evidence(
    context: ProjectContext,
    evidence_id: str,
) -> Evidence:
    from datetime import datetime
    import json
    from analystools.domain.evidence import (
        EvidenceValue,
    )

    store = SQLiteStore(
        context.metadata_path
    )

    store.initialize()

    row = store.get_evidence(
        evidence_id
    )

    if row is None:
        raise ValueError(
            f"Evidence not found: {evidence_id}"
        )

    values_data = json.loads(
        row["values_json"]
    )


    values = [
        EvidenceValue.model_validate(item)
        for item in values_data
    ]

    return Evidence(
        evidence_id=row["evidence_id"],
        run_id=row["run_id"],
        analysis_name=row["analysis_name"],
        dataset=row["dataset"],
        dimensions=json.loads(
            row["dimensions"]
        ),
        metrics=json.loads(
            row["metrics"]
        ),
        sql=row["sql"],
        values=values,
        created_at=datetime.fromisoformat(
            row["created_at"]
        ),
    )


def list_evidence(
    context: ProjectContext,
    analysis_name: str | None = None,
):
    store = SQLiteStore(
        context.metadata_path
    )

    store.initialize()

    return store.list_evidence(
        analysis_name
    )