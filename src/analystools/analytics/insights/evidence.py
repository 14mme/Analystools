from datetime import datetime, timezone
from uuid import uuid4

from analystools.domain.analysis import AnalysisResult
from analystools.domain.evidence import (
    Evidence,
    EvidenceValue,
)


def collect_evidence(
    result: AnalysisResult,
) -> Evidence:
    values: list[EvidenceValue] = []

    column_indexes = {
        column: index
        for index, column in enumerate(
            result.columns
        )
    }

    for row in result.rows:
        dimensions: dict[str, object] = {}
        metrics: dict[str, object] = {}

        for dimension in result.dimensions:
            index = column_indexes.get(dimension)

            if index is None:
                continue

            if index >= len(row):
                continue

            dimensions[dimension] = row[index]

        for metric in result.metrics:
            index = column_indexes.get(metric)

            if index is None:
                continue

            if index >= len(row):
                continue

            metrics[metric] = row[index]

        values.append(
            EvidenceValue(
                dimensions=dimensions,
                metrics=metrics,
            )
        )

    return Evidence(
        evidence_id=str(uuid4()),
        run_id=result.analysis_id,
        analysis_name=result.analysis_name,
        dataset=result.dataset,
        dimensions=result.dimensions,
        metrics=result.metrics,
        sql=result.sql,
        values=values,
        created_at=datetime.now(timezone.utc),
    )