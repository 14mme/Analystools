import typer

from analystools.application.insight_service import (
    generate_insights,
    list_insights,
)
from analystools.application.project_context import (
    discover_project,
)


def generate(
    evidence_id: str = typer.Argument(
        ...,
        help="Evidence ID to analyze.",
    ),
) -> None:
    context = discover_project()

    insights = generate_insights(
        context,
        evidence_id,
    )

    if not insights:
        typer.echo(
            "No insights detected."
        )
        return

    typer.echo(
        f"Detected {len(insights)} insight(s)."
    )

    typer.echo("")

    for insight in insights:
        typer.echo(
            f"[{insight.importance.upper()}] "
            f"{insight.title}"
        )

        typer.echo(
            insight.description
        )

        typer.echo(
            f"Insight ID: "
            f"{insight.insight_id}"
        )

        typer.echo("")


def list_command() -> None:
    context = discover_project()

    insights = list_insights(
        context
    )

    if not insights:
        typer.echo(
            "No insights found."
        )
        return

    for insight in insights:
        typer.echo(
            f"[{insight['importance'].upper()}] "
            f"{insight['title']}"
        )

        typer.echo(
            f"Analysis: "
            f"{insight['analysis_name']}"
        )

        typer.echo(
            f"Evidence: "
            f"{insight['evidence_id']}"
        )

        typer.echo(
            f"Insight ID: "
            f"{insight['insight_id']}"
        )

        typer.echo("")