from analystools.analytics.metrics.sql import quote_identifier
from analystools.domain.analysis import AnalysisDefinition
from analystools.domain.metric import Metric


def build_analysis_sql(
    definition: AnalysisDefinition,
    metrics: list[Metric],
) -> str:
    if len(metrics) != len(definition.metrics):
        raise ValueError(
            "Metric resolution mismatch."
        )

    select_parts: list[str] = []

    for dimension in definition.dimensions:
        select_parts.append(
            quote_identifier(dimension)
        )

    for metric in metrics:
        select_parts.append(
            f"{metric.expression} "
            f'AS {quote_identifier(metric.name)}'
        )

    if not select_parts:
        raise ValueError(
            "Analysis must contain at least one dimension "
            "or metric."
        )

    dataset = quote_identifier(definition.dataset)

    sql = (
        "SELECT\n    "
        + ",\n    ".join(select_parts)
        + f"\nFROM {dataset}"
    )

    if definition.dimensions:
        group_by = ", ".join(
            quote_identifier(dimension)
            for dimension in definition.dimensions
        )

        sql += f"\nGROUP BY {group_by}"

    if definition.order_by:
        order_parts = []

        for item in definition.order_by:
            direction = item.normalized_direction()

            order_parts.append(
                f"{quote_identifier(item.field)} {direction}"
            )

        sql += "\nORDER BY " + ", ".join(order_parts)

    sql += ";"

    return sql