from analystools.analytics.metrics.registry import MetricRegistry
from analystools.application.project_context import ProjectContext
from analystools.domain.metric import Metric


def resolve_metrics(
        context: ProjectContext,
        metric_names: list[str],
) -> list[Metric]:
    registry = MetricRegistry(context)

    metrics: list[Metric] = []

    for name in metric_names:
        metrics.append(registry.get(name))

    return metrics