from datetime import datetime,timezone
from time import perf_counter
from uuid import uuid4

from analystools.analytics.analysis.resolver import (
    resolve_metrics
)
from analystools.analytics.analysis.sql_builder import (
    build_analysis_sql
)
from analystools.application.analysis_loader import (
    load_analysis
)
from analystools.application.project_context import (
    ProjectContext
)
from analystools.domain.analysis import AnalysisResult
from analystools.infrastructure.storage.duckdb import (
    DuckDBStore
)
from analystools.infrastructure.storage.sqlite import (
    SQLiteStore
)


def run_analysis(
        context: ProjectContext,
        analysis_name: str,
) -> AnalysisResult:
    analysis_path = context.analysis_path(
        analysis_name
    )

    definition = load_analysis(analysis_path)

    dataset_path = context.dataset_path(
        definition.dataset
    )

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"DatasetNot Found: {dataset_path}"
        )

    metrics = resolve_metrics(
        context,
        definition.metrics,
    )

    sql = build_analysis_sql(
        definition,
        metrics,
    )

    duckdb_store = DuckDBStore(
        context.warehouse_path
    )

    duckdb_store.register_parquet(
        definition.dataset,
        dataset_path,
    )

    run_id = str(uuid4())
    started_at = datetime.now(
        timezone.utc
    ).isoformat()

    start = perf_counter()

    try:
        columns, rows = duckdb_store.query(sql)

        execution_time_ms = (
            perf_counter() - start
        ) * 1000

        sqlite_store = SQLiteStore(
            context.metadata_path
        )

        sqlite_store.initialize()

        sqlite_store.record_run(
            run_id=run_id,
            analysis_name=definition.name,
            dataet=definition.dataset,
            status="success",
            execution_time_ms=execution_time_ms,
            sql=sql,
            created_at=started_at,
        )

        return AnalysisResult(
            analysis_id=run_id,
            analysis_name=definition.name,
            dataset=definition.dataset,
            dimensions=definition.dimensions,
            metrics=definition.metrics,
            columns=columns,
            rows=rows,
            sql=sql,
            execution_time_ms=execution_time_ms,
        )

    except Exception:
        execution_time_ms = (
            perf_counter() - start
        ) * 1000

        sqlite_store = SQLiteStore(
            context.metadata_path
        )

        sqlite_store.initialize()

        sqlite_store.record_run(
            run_id=run_id,
            analysis_name=definition.name,
            dataet=definition.dataset,
            status="failed",
            execution_time_ms=execution_time_ms,
            sql=sql,
            created_at=started_at,
        )

        raise